use std::{
    fs::File,
    io::Read,
    path::Path,
};
use std::io::{self, BufRead};
use anyhow::Result;
use ndarray::parallel::prelude::*;
use numpy::PyArray2;
use pyo3::create_exception;
use pyo3::prelude::*;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use zip::read::ZipArchive;

#[derive(Serialize, Deserialize)]
struct Batch {
    label: String,
    feature_vector: String,
}


#[derive(Serialize, Deserialize)]
struct Metadata {
    count: usize,
    files: Option<Vec<Batch>>,
    sdk_version: String,
    #[serde(default = "default_batch_size")]
    batch_size: usize,
}

fn default_batch_size() -> usize {
    0
}


fn read_file_from_archive(filepath: &str, arcname: &str) -> Result<String> {
    let file = match File::open(filepath) {
        Ok(file) => file,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open file {}: {}",
                filepath,
                err.to_string()
            ))
        }
    };

    let mut zip = match ZipArchive::new(file) {
        Ok(zip) => zip,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open zip archive {}: {}",
                filepath,
                err.to_string()
            ))
        }
    };

    let mut arcfile = match zip.by_name(arcname) {
        Ok(arcfile) => arcfile,
        Err(err) => {
            return Err(anyhow::anyhow!(
                "Cannot open file {} from archive {}: {}",
                arcname,
                filepath,
                err.to_string()
            ))
        }
    };
    let mut contents = String::new();
    arcfile.read_to_string(&mut contents)?;

    Ok(contents)
}


fn parse_feature_vector_string(fv: &str) -> Vec<f32> {
    fv.strip_prefix("[").unwrap_or(fv)
        .strip_suffix("]").unwrap_or(fv)
        .split(",")
        .map(|x| x.trim().parse::<f32>().unwrap())
        .collect()
}


fn parse_feature_vector_string_to_ndarray(fv: &str) -> ndarray::Array1::<f32> {
    fv.strip_prefix("[").unwrap_or(fv)
        .strip_suffix("]").unwrap_or(fv)
        .split(",")
        .map(|x| x.trim().parse::<f32>().unwrap())
        .collect()
}


fn parse_feature_vectors(feature_vectors: Vec<&str>) -> Vec<Vec<f32>> {
    feature_vectors
        .into_par_iter()
        .map(|fv| parse_feature_vector_string(fv))
        .collect()
}


fn read_batch(batch: &Batch, filepath: &str, slice_labels: &mut [String], mut slice_features: ndarray::ArrayViewMut<f32, ndarray::Dim<[usize; 2]>>) -> Result<()>{
    // use buffer read file to avoid load whole file into memory
    // https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html#a-more-efficient-approach
    // open the file from the very start
    // as it is running in parallel we should be good to go
    let path = Path::new(filepath);
    let labels_zip_archive_file = File::open(&path)?;
    let features_zip_archive_file = File::open(&path)?;
    let mut labels_zip_archive = ZipArchive::new(labels_zip_archive_file)?;
    let mut features_zip_archive = ZipArchive::new(features_zip_archive_file)?;
    let (
        labels_file,
        features_file,
    )  = (
        labels_zip_archive.by_name(&batch.label)?,
        features_zip_archive.by_name(&batch.feature_vector)?,
    );

    io::BufReader::new(labels_file).lines()
    .zip(io::BufReader::new(features_file).lines())
    .enumerate()
    .for_each(|(idx, (label, fv))| {
        slice_labels[idx] = label.unwrap().to_string();
        slice_features.row_mut(idx).assign(&parse_feature_vector_string_to_ndarray(&fv.unwrap())); // .assign(&parse_feature_vector_string_to_ndarray(&fv.unwrap()));
    });
    Ok(())
}


fn unpack_internal(filepath: &str) -> Result<(Vec<String>, ndarray::ArrayBase<ndarray::OwnedRepr<f32>, ndarray::Dim<[usize; 2]>>)> {
    // Open the zip archive
    let metadata_str = read_file_from_archive(filepath, "meta.json")?;
    let metadata: Metadata = serde_json::from_str(&metadata_str)?;

    let feature_vectors_count = metadata.count;

    if feature_vectors_count == 0 {
        return Ok((Vec::new(), ndarray::Array2::<f32>::zeros((0, 512))));
    }

    let default_batch = Batch {
        label: "labels.txt".to_string(),
        feature_vector: "features.txt".to_string(),
    };

    let mut batches: Vec<&Batch> = Vec::new();

    let files = metadata.files.unwrap_or_default();
    for batch in files.iter() {
        batches.push(batch);
    }


    let mut batch_size = metadata.batch_size;
    if batches.len() == 0 {
        // support older versions of rcdb versions, like generated from fvm
        batches.push(&default_batch);
        batch_size = metadata.count;
    }
    println!("{}", batch_size);

    // allocate memory for results
    let mut labels: Vec<String> = vec!["".into(); feature_vectors_count];
    let mut array_features = ndarray::Array2::<f32>::zeros((feature_vectors_count, 512));

    let axis_chunks_iter_mut: ndarray::iter::AxisChunksIterMut<f32, ndarray::Dim<[usize; 2]>>  = array_features.axis_chunks_iter_mut(ndarray::Axis(0), batch_size);
    labels
    .par_chunks_mut(batch_size)
    .zip(axis_chunks_iter_mut.into_par_iter())
    .enumerate()
    .for_each(|(batch_index, (slice_labels, slice_features))| {
        let _ = read_batch(batches[batch_index], filepath, slice_labels, slice_features);
    });

    Ok((labels, array_features))
}


/// rust usage only
pub fn unpack(filepath: &str) -> Result<(Vec<String>, ndarray::Array2<f32>)> {
    Ok(unpack_internal(filepath).unwrap())
}


create_exception!(rcdb_unpacker, RcdbUnpackerError, pyo3::exceptions::PyException);

#[pymodule]
fn rcdb_unpacker(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("RcdbUnpackerError", _py.get_type::<RcdbUnpackerError>())?;

    /// Unpacks the RCDB file and returns labels and features np.ndarray
    /// supply with filepath to the rcdb file
    #[pyfn(m)]
    fn unpack<'py>(py: Python<'py>, filepath: &str) -> PyResult<(Vec<String>, &'py PyArray2<f32>)> {
        match unpack_internal(filepath) {
            Ok((labels, features)) => Ok((labels, PyArray2::from_owned_array(py, features))),
            Err(err) => Err(RcdbUnpackerError::new_err(err.to_string())),
        }
    }

    /// parse list of string representation of feature vectors
    /// [fv, fv, fv, ...]
    /// where fv can be in either formats:
    /// [1.0, 2.0, 3.0, ...], or
    /// 1.0, 2.0, 3.0, ...
    /// returns np.ndarray
    #[pyfn(m)]
    fn parse_fvs<'py>(py: Python<'py>, feature_vectors: Vec<&str>) -> PyResult<&'py PyArray2<f32>> {
        let features = parse_feature_vectors(feature_vectors);
        Ok(PyArray2::from_vec2(py, &features).unwrap())
    }

    Ok(())
}


#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use super::*;

    #[test]
    fn can_read_zero_size_rcdb() {
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("zeta_export.rcdb");
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 0),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn can_read_symphony_rcdb() {
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("symphony_137_fvs.rcdb");
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 137),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn can_read_symphony_rcdb_with_batches() {
        let mut d = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        d.push("resources");
        d.push("symphony_137_fvs_batch_20.rcdb");
        println!("path: {:#?}", d.display());

        let _ = match unpack_internal(d.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 137),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn can_read_feature_vectors_with_spaces() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("reference_db.rcdb");  // file with spaces
        println!("path: {:#?}", path_buf.display());

        let _ = match unpack_internal(path_buf.to_str().unwrap()) {
            Ok((labels, _features)) => assert_eq!(labels.len(), 43),
            Err(err) => panic!("Error: {}", err),
        };
    }

    #[test]
    fn internal_unpack_format() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("symphony_137_fvs.rcdb");
        println!("path: {:#?}", path_buf.display());

        let (labels, features) = match unpack(path_buf.to_str().unwrap()) {
            Ok((labels, features)) => (labels, features),
            Err(err) => panic!("Error: {}", err),
        };
        assert_eq!(labels.len(), 137);
        assert_eq!(features.shape(), &[137, 512]);
    }

    #[test]
    fn raise_exception_when_no_file_found() {
        let mut path_buf = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        path_buf.push("resources");
        path_buf.push("non_existing_file.rcdb");
        println!("path: {:#?}", path_buf.display());

        let _ = match unpack_internal(path_buf.to_str().unwrap()) {
            Ok((_labels, _features)) => {},
            Err(err) => assert!(err.to_string().contains("Cannot open file")),
        };
    }

    #[test]
    fn parse_feature_vector_string_test() {
        let fv = "[1.0, 2.0, 3.0]";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);

        let fv = "1.0, 2.0, 3.0";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);

        let fv = "1.0,2.0,3.0";
        let parsed = parse_feature_vector_string(fv);
        assert_eq!(parsed, vec![1.0, 2.0, 3.0]);
    }

    #[test]
    fn parse_feature_vectors_test() {
        let fvs = vec!["[1.0, -2.0, 3.0]", "1.0, -2.0, 3.0", "1.0,-2.0,3.0"];
        let parsed = parse_feature_vectors(fvs);
        assert_eq!(parsed, vec![vec![1.0, -2.0, 3.0], vec![1.0, -2.0, 3.0], vec![1.0, -2.0, 3.0]]);
    }
}

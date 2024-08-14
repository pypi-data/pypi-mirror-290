use pyo3::prelude::*;
mod mouse;
mod browser;
mod screenshot;
mod mask;

#[pyfunction]
fn get_name() -> String {
    "whatpack".to_string()
}


#[pymodule]
fn whatpack_backend(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<mouse::MouseControl>()?;
    m.add_class::<browser::BrowserTracker>()?;
    m.add_function(wrap_pyfunction!(browser::open_whatsapp, m)?)?;
    m.add_function(wrap_pyfunction!(get_name, m)?)?;
    m.add_function(wrap_pyfunction!(screenshot::py_screenshot, m)?)?;
    m.add_function(wrap_pyfunction!(mask::mask_file_py, m)?)?;
    m.add_function(wrap_pyfunction!(mask::capture_and_mask, m)?)?;
    Ok(())
}
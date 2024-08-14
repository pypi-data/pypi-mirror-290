use pyo3::prelude::*;
use mouse_rs::{Mouse};
use std::sync::{Arc, Mutex};
use mouse_rs::{types::keys::Keys};

#[pyclass]
pub struct MouseControl {
    mouse: Arc<Mutex<Mouse>>,
}

#[pymethods]
impl MouseControl {
    #[new]
    fn new() -> Self {
        MouseControl {
            mouse: Arc::new(Mutex::new(Mouse::new())),
        }
    }

    fn move_mouse(&self, x: i32, y: i32) -> PyResult<()> {
        let mouse = self.mouse.lock().map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Failed to lock mouse"))?;
        mouse.move_to(x, y).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to move mouse: {:?}", e)))?;
        Ok(())
    }

    fn get_mouse_position(&self) -> PyResult<(i32, i32)> {
        let mouse = self.mouse.lock().map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Failed to lock mouse"))?;
        let point = mouse.get_position().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to get mouse position: {:?}", e)))?;
        Ok((point.x, point.y))
    }

    fn click(&self,key:String) -> PyResult<()> {
        let mouse = self.mouse.lock().map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Failed to lock mouse"))?;
        let key = match key.as_str() {
            "left" => Keys::LEFT,
            "right" => Keys::RIGHT,
            "middle" => Keys::MIDDLE,
            _ => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid key")),
        };
        mouse.click(&key).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to click mouse: {:?}", e)))?;
        Ok(())
    }

}
unsafe impl Send for MouseControl {}
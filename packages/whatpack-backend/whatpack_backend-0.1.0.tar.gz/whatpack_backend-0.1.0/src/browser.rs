use xcap::Window;
use pyo3::prelude::*;

#[pyclass]
pub struct BrowserTracker {
    x: i32,
    y: i32,
    width: u32,
    height: u32,
    browsers: Vec<String>,
}

#[pymethods]
impl BrowserTracker {
    #[new]
    fn new() -> Self {
        BrowserTracker {
            x: 0,
            y: 0,
            width: 0,
            height: 0,
            browsers: Vec::new(),
        }
    }

    fn get_browsers_list(&mut self) -> PyResult<Vec<String>> {
        let browsers_list = vec!["chrome", "firefox", "brave", "chromium"];
        let windows = Window::all().unwrap();
        let mut browsers = Vec::new();

        for window in windows {
            let title = window.app_name();
            println!("Title: {}", title);
            let browser = browsers_list.iter().find(|&b| title.to_lowercase().contains(b));
            if let Some(b) = browser {
                browsers.push(b.to_string());

                self.x = window.x();
                self.y = window.y();
                self.width = window.width();
                self.height = window.height();
            }
        }
        self.browsers = browsers.clone();
        Ok(browsers)
    }

    fn get_position(&mut self) -> PyResult<(i32, i32)> {
        Ok((self.x, self.y))
    }
    
    fn get_dimensions(&mut self) -> PyResult<(u32, u32)> {
        Ok((self.width, self.height))
    }


    fn get_stored_browsers(&self) -> PyResult<Vec<String>> {
        Ok(self.browsers.clone())
    }

    fn get_browser_details(&self,name: String) -> PyResult<(i32, i32, u32, u32)> {
        let windows = Window::all().unwrap();
        let mut x = 0;
        let mut y = 0;
        let mut width = 0;
        let mut height = 0;

        for window in windows {
            let title = window.app_name();
            if title.to_lowercase().contains(&name) {
                x = window.x();
                y = window.y();
                width = window.width();
                height = window.height();
            }
        }
        Ok((x, y, width, height))
    }
}

#[pyfunction]
#[pyo3(signature = (browser= None, number=None,message=None))]
pub fn open_whatsapp(browser:Option<String>,number:Option<String>,message:Option<String>) -> PyResult<()> {
    let url = if number.is_some() && message.is_some() {
        format!("https://web.whatsapp.com/send?phone={}&text={}", number.unwrap(), message.unwrap())
    } else {
        "https://web.whatsapp.com".to_string()
    };
    let _ = open::with(url,browser.unwrap_or_else(|| "chrome".to_string()));
    Ok(())
}
use xcap::Window;
use pyo3::prelude::*;
use image::{Rgb, Rgba};
use image::ImageBuffer;
use std::path::Path;

fn rgba8_to_rgb8(input: image::ImageBuffer<Rgba<u8>, Vec<u8>>) -> image::ImageBuffer<Rgb<u8>, Vec<u8>> {
    let width = input.width() as usize;
    let height = input.height() as usize;
    let input: &Vec<u8> = input.as_raw();
    let mut output_data = vec![0u8; width * height * 3];
    
    let mut i = 0;
    for chunk in input.chunks(4) {
        output_data[i..i+3].copy_from_slice(&chunk[0..3]);
        i+=3;
    }
    
    image::ImageBuffer::from_raw(width as u32, height as u32, output_data).unwrap()
}

#[pyfunction]
#[pyo3(signature = (browser= None, save_file=None))]
pub fn py_screenshot(browser: Option<String>,save_file:Option<String>) -> PyResult<()> {
    let save_file = save_file.unwrap_or_else(|| "screenshot.png".to_string());
    let _ = screenshot(browser,Some(save_file));
    Ok(())
}


pub fn screenshot(browser: Option<String>, save_file: Option<String>) -> Result<ImageBuffer<Rgb<u8>, Vec<u8>>, Box<dyn std::error::Error>> {
    let browser_name = browser.unwrap_or_else(|| "chrome".to_string());
    let windows = Window::all()?;
    let mut save = false;
    if save_file.is_some() {
        println!("Saving screenshot to: {}", save_file.as_ref().unwrap());
        save = true;
    }
    for window in windows {
        let title = window.app_name();
        if title.to_lowercase().contains(&browser_name.to_lowercase()) {
            let screenshot = window.capture_image()?;
            let rgb_screenshot = rgba8_to_rgb8(screenshot);

            if save {
                let file = Path::new(save_file.as_ref().unwrap());
                rgb_screenshot.save(file)?;
                return Ok(rgb_screenshot);
            }
            else {
                return Ok(rgb_screenshot);
            }
        }
    }

    Err("No matching window found".into())
}

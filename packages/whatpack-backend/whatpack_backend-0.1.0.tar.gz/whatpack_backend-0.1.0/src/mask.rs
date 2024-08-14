use image::{ImageBuffer, Rgb};
use pyo3::prelude::*;
use crate::screenshot::screenshot;
use std::path::Path;

#[pyfunction]
#[pyo3(signature = (image_path="screenshot.jpg", mask_path="masked_image.jpg",top_height=None,bottom_height=None,left_width=None,right_width=None))]
pub fn mask_file_py(image_path: &str,mask_path: &str,top_height:Option<u32>,bottom_height:Option<u32>,left_width:Option<u32>,right_width:Option<u32>) -> PyResult<()> {
    mask_file(image_path,mask_path,top_height,bottom_height,left_width,right_width);
    Ok(())
}

fn mask_image(image: ImageBuffer<Rgb<u8>, Vec<u8>>,top_height:Option<u32>,bottom_height:Option<u32>,left_width:Option<u32>,right_width:Option<u32>,width:Option<u32>,height:Option<u32>) -> ImageBuffer<Rgb<u8>, Vec<u8>> {
    let (width2, height2) = image.dimensions();
    let width = width.unwrap_or(width2 as u32);
    let height = height.unwrap_or(height2 as u32);
    let mut masked_image = ImageBuffer::new(width, height);
    let top_height = top_height.unwrap_or((height as f32 * 0.6) as u32);
    let left_width = left_width.unwrap_or((width as f32 * 0.3) as u32);
    let right_width = right_width.unwrap_or((width as f32 * 0.5) as u32);
    let bottom_height = bottom_height.unwrap_or(0 as u32);
    for (x, y, pixel) in image.enumerate_pixels() {
        let masked_pixel = if y < top_height || x < left_width || x > right_width || y > height - bottom_height {
           Rgb([0 as u8, 0 as u8, 0 as u8])
        }
        else {
            *pixel
        };

        masked_image.put_pixel(x, y, masked_pixel);
    }

    masked_image
}

fn mask_file(image_path: &str, mask_path: &str,top_height:Option<u32>,bottom_height:Option<u32>,left_width:Option<u32>,right_width:Option<u32>) {
    let image = image::open(image_path).expect("Failed to open image").to_rgb8();
    let (width, height) = image.dimensions();
    let top_height = top_height.unwrap_or((height as f32 * 0.6) as u32);
    let left_width = left_width.unwrap_or((width as f32 * 0.3) as u32);
    let right_width = right_width.unwrap_or((width as f32 * 0.5) as u32);
    let bottom_height = bottom_height.unwrap_or(0 as u32);
    let masked_image = mask_image(image, Some(top_height),Some(bottom_height), Some(left_width), Some(right_width),Some(width),Some(height));
    let mask_path = Path::new(mask_path);
    masked_image.save(mask_path).expect("Failed to save masked image");
}


#[pyfunction]
#[pyo3(signature = (browser=None, save_file=None, mask_path=None))]
pub fn capture_and_mask(browser: Option<String>, save_file: Option<String>, mask_path: Option<String>) {
    let image = screenshot(browser,save_file).expect("Failed to capture screenshot");
    let mask = mask_image(image, None, None, None, None, None, None);
    let binding = mask_path.unwrap_or(String::from("masked_image.jpg"));
    let mask_path = Path::new(&binding);
    mask.save(mask_path).expect("Failed to save masked image");
}


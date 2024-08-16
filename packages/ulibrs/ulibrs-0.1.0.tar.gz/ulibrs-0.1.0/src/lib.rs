use pyo3::prelude::*;

#[pyfunction]
fn add(a: usize, b: usize) -> usize {
    ::ulibrs::add(a, b)
}

#[pymodule]
fn ulibrs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}

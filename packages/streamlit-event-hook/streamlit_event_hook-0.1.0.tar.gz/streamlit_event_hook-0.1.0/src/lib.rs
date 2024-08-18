use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// 获取函数对象，入参格式：inspect.getsource
fn get_func<'a>(py: Python<'a>, func: &str) -> PyResult<Bound<'a, PyAny>> {
    if let Some((module_path, name)) = func.rsplit_once('.') {
        let func_obj = PyModule::import_bound(py, module_path)?.getattr(name)?;
        Ok(func_obj)
    } else {
        Err(PyTypeError::new_err("Invalid function path"))
    }
}

fn hook_func(py: Python, func_obj: Bound<PyAny>,
             before_func: Option<&str>, before_func_args: Option<&str>,
             after_func: Option<&str>, after_func_args: Option<&str>) -> PyResult<()> {
    let getsource = get_func(py, "inspect.getsource")?;
    let func_name = func_obj.getattr("__name__")?.str()?.to_string();
    let new_func_name = format!("__hook__{}", func_name);
    let source_code = getsource.call1((&func_obj, ))?.str()?.to_string();
    let new_source_code = source_code.replace(&format!("def {}", func_name), &format!("def {}", new_func_name));
    let new_source_code = new_source_code
        .lines()
        .map(|line| format!("    {}", line))
        .collect::<Vec<String>>()
        .join("\n");
    let offset_str = &source_code[..source_code.find("def").unwrap_or(0)];
    let before_func_code = match before_func {
        None => "".to_string(),
        Some(before_func) => {
            let (module_path, name) = before_func.rsplit_once(".")
                .ok_or_else(|| PyTypeError::new_err("Invalid function path"))?;
            let func_args = before_func_args.unwrap_or_else(|| "");
            format!("{offset_str}    from {module_path} import {name}\n{offset_str}    {name}({func_args})")
        }
    };
    let after_func_code = match after_func {
        None => "".to_string(),
        Some(after_func) => {
            let (module_path, name) = after_func.rsplit_once(".")
                .ok_or_else(|| PyTypeError::new_err("Invalid function path"))?;
            let func_args = after_func_args.unwrap_or_else(|| "");
            format!("{offset_str}    from {module_path} import {name}\n{offset_str}    {name}({func_args})")
        }
    };

    let new_code = format!(r#"
{offset_str}def {func_name}(*args, **kwargs):
{new_source_code}
{before_func_code}
{offset_str}    __hook__result = {new_func_name}(*args, **kwargs)
{after_func_code}
{offset_str}    return __hook__result
    "#).trim_start_matches("\n").to_owned();

    let patchy_replace = get_func(py, "patchy.replace")?;
    let kwargs = [("expected_source", source_code), ("new_source", new_code)].into_py_dict_bound(py);
    patchy_replace.call((func_obj,), Some(&kwargs))?;

    Ok(())
}

#[pyfunction]
fn hook(before_render: Option<String>, after_render: Option<String>, event_handler: Option<String>) -> PyResult<()> {
    Python::with_gil(|py| {
        // let before_func = std::env::var("BEFORE_FUNC").ok();

        let exec_func_with_error_handling = get_func(py, "streamlit.runtime.scriptrunner.exec_code.exec_func_with_error_handling")?;
        hook_func(py, exec_func_with_error_handling,
                  before_render.as_deref(), None,
                  after_render.as_deref(), None)?;

        let _handle_scriptrunner_event_on_event_loop = PyModule::import_bound(py, "streamlit.runtime.app_session")?
            .getattr("AppSession")?.getattr("_handle_scriptrunner_event_on_event_loop")?;
        hook_func(py, _handle_scriptrunner_event_on_event_loop, None, None, event_handler.as_deref(), Some("sender=args[1], event=args[2], forward_msg=args[3]"))?;

        Ok(())
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn streamlit_event_hook(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(hook, m)?)?;
    Ok(())
}

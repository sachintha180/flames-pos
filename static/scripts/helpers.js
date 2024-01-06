async function postJSON(routeURL, jsonObject) {
  try {
    const response = await fetch(routeURL, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(jsonObject),
    })
    const result = await response.json()
    return result
  } catch (error) {
    return error
  }
}

function showError(errorMessage, errorAction, success = false) {
  const errorModal = document.querySelector('#error')
  const errorSubtitle = document.querySelector('#error_type')

  let errorType = 'FlamesPOS Error'
  errorSubtitle.style.backgroundColor = 'var(--error)'

  if (success) {
    errorType = 'FlamesPOS Success'
    errorSubtitle.style.backgroundColor = 'var(--success)'
  }

  const errorTitle = document.querySelector('#error_title')
  const errorLbl = document.querySelector('#error_lbl')

  errorTitle.innerHTML = errorMessage
  errorSubtitle.innerHTML = errorType
  errorLbl.innerHTML = errorAction

  errorModal.setAttribute('open', true)
}

function hideError() {
  const errorTitle = document.querySelector('#error_title')
  const errorSubtitle = document.querySelector('#error_type')
  const errorLbl = document.querySelector('#error_lbl')

  const errorModal = document.querySelector('#error')

  errorTitle.innerHTML = ''
  errorSubtitle.innerHTML = ''
  errorLbl.innerHTML = ''

  errorModal.removeAttribute('open')
}

function setBtnBusy(btn, busy) {
  if (busy) {
    btn.setAttribute('aria-busy', 'true')
  } else {
    btn.removeAttribute('aria-busy')
  }
}

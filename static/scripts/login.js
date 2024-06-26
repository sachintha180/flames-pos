function handleAuth() {
  hideError()
  const username = document.querySelector('#username').value
  const password = document.querySelector('#password').value

  const submitBtn = document.querySelector('#submit')
  setBtnBusy(submitBtn, true)

  if (username && password) {
    postJSON('/login', {
      username: username,
      password: password,
    }).then((response) => {
      showError(response.message, response.action, response.data.flag)
      if (response.data.flag) {
        window.location.href = '/menu'
      }
    })
  } else {
    if (!username) {
      showError('Invalid username', 'Please enter a valid username')
    } else {
      showError('Invalid password', 'Please enter a valid password')
    }
  }

  setBtnBusy(submitBtn, false)
}

document.addEventListener('DOMContentLoaded', () => {
  showError(
    'You have logged out',
    'Please login to FlamesPOS again to continue',
    false
  )

  const submitBtn = document.querySelector('#submit')
  submitBtn.addEventListener('click', handleAuth)

  const errorCloseBtn = document.querySelector('#error_close')
  errorCloseBtn.addEventListener('click', hideError)
})

function handleBilling() {
  const billingBtn = document.querySelector('#billing_btn')
  setBtnBusy(billingBtn, true)
  window.location.href = '/billing'
  setBtnBusy(billingBtn, false)
}

document.addEventListener('DOMContentLoaded', () => {
  const billingBtn = document.querySelector('#billing_btn')
  billingBtn.addEventListener('click', handleBilling)
})

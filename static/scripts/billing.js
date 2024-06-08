const CATEGORIES = [
  'All',
  'Pizzas',
  'Pastas',
  'Toppings',
  'Salads',
  'Appetizers',
]
const VAT_PERCENT = 0.18
const SERVICE_CHARGE_PERCENT = 0.05
let PENDING_ORDERS = {}

function addItem(id, name, price, quantity) {
  const itemContainer = document.querySelector('#item-rows')
  let item = document.createElement('div')
  item.classList.add('item')
  item.innerHTML += `<p class="id">${id}</p>`
  item.innerHTML += `<p class="name">${name}</p>`
  item.innerHTML += `<p class="price">${price}</p>`
  item.innerHTML += `<p class="quantity">${quantity}</p>`
  item.innerHTML += `<button type="button" class="quantity-btn" name="remove">-</button>`
  itemContainer.append(item)
}

function toggleProductCategory(category) {
  const products = document.querySelectorAll('#product-items .product')
  products.forEach((product) => {
    if (product.classList.contains(category) || category === 'category-0') {
      product.style.display = 'flex'
    } else {
      product.style.display = 'none'
    }
  })
}

function zeroBillTotals() {
  totalLabels = document.querySelectorAll('#total .total-row :not(.item-label)')
  totalLabels.forEach((totalLabel) => {
    totalLabel.innerHTML = 'Rs. 0.00'
  })
}

function updateBillItemQuantity(itemID, billItems) {
  const itemContainer = document.querySelector('#item-rows')
  const existingItems = itemContainer.querySelectorAll('.item')

  let updated = false
  let itemIndex = 0
  while (itemIndex < existingItems.length && !updated) {
    if (existingItems[itemIndex].id === itemID) {
      if (billItems[itemID].quantity == 0) {
        existingItems[itemIndex].remove()
      } else {
        existingItems[itemIndex].querySelector('.quantity').innerHTML =
          billItems[itemID].quantity
      }
      updated = true
    }
    itemIndex++
  }

  return updated
}

function createBillItem(id, name, price, quantity) {
  let item = document.createElement('div')
  item.classList.add('item')
  item.id = id
  item.innerHTML += `<p class="id">${id}</p>`
  item.innerHTML += `<p class="name">${name}</p>`
  item.innerHTML += `<p class="price">Rs. ${price}</p>`
  item.innerHTML += `<p class="quantity">${quantity}</p>`
  item.innerHTML += `<button type="button" class="quantity-btn" name="remove">-</button>`
  return item
}

function setBillItem(itemID, billItems) {
  const itemContainer = document.querySelector('#item-rows')
  const existingItems = itemContainer.querySelectorAll('.item')

  if (existingItems.length == 0) {
    itemContainer.innerHTML = ''
  }
  const updated = updateBillItemQuantity(itemID, billItems)

  if (!updated) {
    const billItem = createBillItem(
      itemID,
      billItems[itemID].name,
      billItems[itemID].price,
      billItems[itemID].quantity
    )
    billItem.querySelector('.quantity-btn').addEventListener('click', () => {
      billItems[itemID].quantity--
      updateBillItemQuantity(itemID, billItems)
      if (billItems[itemID].quantity === 0) {
        delete billItems[itemID]
      }
    })
    itemContainer.append(billItem)
  }

  return billItems
}

function addBillItem(itemDetails, billItems) {
  if (itemDetails.id in billItems) {
    billItems[itemDetails.id].quantity++
  } else {
    billItems[itemDetails.id] = {
      name: itemDetails.name,
      price: itemDetails.price,
      quantity: itemDetails.quantity,
    }
  }
  billItems = setBillItem(itemDetails.id, billItems)
  return billItems
}

function calculateTotals(billItems) {
  let subtotal = 0
  for (let key in billItems) {
    subtotal += billItems[key].price * billItems[key].quantity
  }
  const discount = 0
  const service_charge = subtotal * SERVICE_CHARGE_PERCENT
  const value_added_tax = subtotal * VAT_PERCENT
  const delivery_charge = 0
  const total =
    subtotal + discount + service_charge + value_added_tax + delivery_charge

  return {
    subtotal: subtotal,
    discount: discount,
    service_charge: service_charge,
    value_added_tax: value_added_tax,
    delivery_charge: delivery_charge,
    total: total,
  }
}

function displayTotals(totalObject) {
  document.querySelector(
    '#subtotal'
  ).innerHTML = `Rs. ${totalObject.subtotal.toFixed(2)}`
  document.querySelector(
    '#discount'
  ).innerHTML = `Rs. ${totalObject.discount.toFixed(2)}`
  document.querySelector(
    '#service_charge'
  ).innerHTML = `Rs. ${totalObject.service_charge.toFixed(2)}`
  document.querySelector(
    '#value_added_tax'
  ).innerHTML = `Rs. ${totalObject.value_added_tax.toFixed(2)}`
  document.querySelector(
    '#delivery_charge'
  ).innerHTML = `Rs. ${totalObject.delivery_charge.toFixed(2)}`
  document.querySelector(
    '#bill-total'
  ).innerHTML = `Rs. ${totalObject.total.toFixed(2)}`
}

function resetBill() {
  zeroBillTotals()
  document.querySelector(
    '#item-rows'
  ).innerHTML = `<p class="temp-msg">Start bill by adding products</p>`
}

function showPendingOrders() {
  const pendingContainer = document.querySelector('#pending-list')
  pendingContainer.innerHTML = ''
  for (let key in PENDING_ORDERS) {
    let pendingItem = document.createElement('div')
    pendingItem.classList.add('pending-order')
    pendingItem.innerHTML += `<p class="pending-order-id">Order ID: #${key}</p>`
    pendingContainer.appendChild(pendingItem)
  }
}

function handleSave(billItems, totalObject) {
  hideError()

  const saveBtn = document.querySelector('#save')
  setBtnBusy(saveBtn, true)

  if (Object.keys(billItems).length == 0) {
    showError('Invalid bill', 'Please add one or more items to save the bill')
  } else if (Object.keys(totalObject).total <= 0) {
    showError(
      'Invalid total',
      'Please add items to the bill, the bill total is invalid'
    )
  } else {
    postJSON('/save_order', {
      totals: totalObject,
      items: billItems,
    }).then((response) => {
      showError(response.message, response.action, response.data.flag)
      if (response.data.flag) {
        resetBill()
        PENDING_ORDERS[response.data.order_id] = {
          totalObject: billItems,
          billItems: totalObject,
        }
        showPendingOrders()
      }
    })
  }

  setBtnBusy(saveBtn, false)
}

document.addEventListener('DOMContentLoaded', () => {
  let billItems = {}
  let totalObject = {}
  zeroBillTotals()

  const categoryBtns = document.querySelectorAll('#product-header .category')
  categoryBtns.forEach((categoryBtn) => {
    categoryBtn.addEventListener('click', () => {
      toggleProductCategory(categoryBtn.classList[1])
    })
  })

  const productBtns = document.querySelectorAll('#product-items .product')
  productBtns.forEach((productBtn) => {
    productBtn.addEventListener('click', () => {
      billItems = addBillItem(
        {
          id: productBtn.querySelector('.id').innerHTML.slice(1),
          name: productBtn.querySelector('.name').innerHTML,
          price: parseFloat(
            parseFloat(productBtn.querySelector('.price').innerHTML.slice(3))
          ),
          quantity: 1,
        },
        billItems
      )
      totalObject = calculateTotals(billItems)
      displayTotals(totalObject)
    })
  })

  const saveBtn = document.querySelector('#save')
  saveBtn.addEventListener('click', () => {
    handleSave(billItems, totalObject)
    totalObject = {}
    billItems = {}
  })

  const errorCloseBtn = document.querySelector('#error_close')
  errorCloseBtn.addEventListener('click', hideError)
})

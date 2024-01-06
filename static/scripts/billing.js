const CATEGORIES = [
  'All',
  'Pizzas',
  'Pastas',
  'Toppings',
  'Salads',
  'Appetizers',
]

function addItem(id, name, price, quantity) {
  const itemContainer = document.querySelector('#item-rows')
  let item = document.createElement('div')
  item.classList.add('item')
  item.innerHTML += `<p class="id">${id}</p>`
  item.innerHTML += `<p class="name">${name}</p>`
  item.innerHTML += `<p class="price">${price}</p>`
  item.innerHTML += `<p class="quantity">${quantity}</p>`
  item.innerHTML += `<button type="button" class="quantity-btn" name="remove">-</button>`
  item.innerHTML += `<button type="button" class="quantity-btn" name="add">+</button>`
  itemContainer.append(item)
}

function addProduct(id, name, imageAlt, imageSrc, price) {
  const productContainer = document.querySelector('#product-items')
  let product = document.createElement('div')
  product.classList.add('product')
  product.innerHTML += `<p class="id">#${id}</p>`
  product.innerHTML += `<p class="name">${name}</p>`
  product.innerHTML += `<img alt="${imageAlt}" src="${imageSrc}" height="100">`
  product.innerHTML += `<p class="price">${price}</p>`
  productContainer.append(product)
}

function addProductCategories(categories) {
  const productHeader = document.querySelector('#product-header')
  categories.forEach((category) => {
    productHeader.innerHTML += `<p class="category">${category}</p>`
  })
}

document.addEventListener('DOMContentLoaded', () => {
  addProductCategories(CATEGORIES)
  for (let i = 0; i < 100; i++) {
    addItem(i, 'item.name', 'item.price', Math.floor(Math.random() * 100 + 10))
    addProduct(
      i,
      'product.name',
      'image.alt',
      'static/icons/triangle.svg',
      Math.floor(Math.random() * 10000 + 10000)
    )
  }
})

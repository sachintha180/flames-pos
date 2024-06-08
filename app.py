from flask import Flask, render_template, request, session, redirect
from models import Customer, Order, OrderProduct, Payment, Product, Staff, db, User
from helpers import (
    generate_response,
    get_random_quote,
    validate_attributes,
    login_required,
)
from flask_bcrypt import generate_password_hash, check_password_hash
import enums, random
from data import product_names, product_descriptions
from faker import Faker

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

# initialize models.py SQLAlchemy object
db.init_app(app)

# note: db.create_all() only creates models if they don't exist
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():
    return redirect("login")


# note: /initialize route is NOT PUBLICLY visible
@app.route("/initialize", methods=["GET", "POST"])
def initialize():
    if request.method == "GET":
        return render_template("initialize.html", version=app.config.get("VERSION"))
    else:
        # verify the provided credentials against the superadmin's credentials
        response = validate_attributes(
            request.json,
            ["username", "password"],
            app.config.get("SUPERADMIN_DEFAULT"),
        )
        if response.status_code != 200:
            return response

        # return HTML with owner's default credentials
        return generate_response(
            status_code=200,
            message="Login successful",
            action=f"You are now authenticated as '{request.json['username']}'",
            data={
                "html": render_template(
                    "manage.html", owner_default=app.config.get("OWNER_DEFAULT")
                ),
                "flag": True,
            },
        )


# note: /add_owner route is NOT PUBLICLY visible
@app.route("/add_owner", methods=["POST"])
def addOwner():
    if request.method == "POST":
        # validate the presence of User model attributes in payload
        response = validate_attributes(
            request.json, ["username", "password", "fullname", "mobile_no"]
        )
        if response.status_code != 200:
            return response

        # query username in database
        try:
            query = db.session.select(User).where(User.username == request.json["username"]).where(User.role == enums.UserRole.owner)
            matched_users = db.session.scalars(query).all()
            print(matched_users)
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to check owner",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # check if provided username already exists
        if len(matched_users) > 0:
            return generate_response(
                status_code=400,
                message="Owner already exists",
                action="Please try again with a different username",
                data={"flag": False},
            )

        # otherwise, create and insert owner into database
        try:
            owner = User(
                username=request.json["username"],
                password=generate_password_hash(request.json["password"]),
                fullname=request.json["fullname"],
                mobile_no=request.json["mobile_no"],
                role=enums.UserRole.owner.value,
            )
            db.session.add(owner)
            db.session.commit()
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to add owner",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # otherwise, return success JSON
        return generate_response(
            status_code=200,
            message="Successfully added owner",
            action=f"You have now added the owner '{request.json['username']}'",
            data={"flag": True},
        )


# note: /reset_db route is NOT PUBLICLY visible
@app.route("/reset_db", methods=["POST"])
def resetDB():
    if request.method == "POST":
        # verify the provided credentials against the superadmin's credentials
        response = validate_attributes(
            request.json,
            ["username", "password"],
            app.config.get("SUPERADMIN"),
        )
        if response.status_code != 200:
            return response

        # delete and re-initialize schema + clear schema
        try:
            db.drop_all()
            db.create_all()
            session.clear()
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to reset database",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # return success JSON
        return generate_response(
            status_code=200,
            message="Successfully reset database",
            action=f"You have now reset the database",
            data={"flag": True},
        )


# note: /fill_rnd route is NOT PUBLICLY visible
@app.route("/fill_rnd", methods=["POST"])
def fillRnd():
    if request.method == "POST":
        # verify the provided credentials against the superadmin's credentials
        response = validate_attributes(
            request.json,
            ["username", "password"],
            app.config.get("SUPERADMIN"),
        )
        if response.status_code != 200:
            return response

        # initialize maximum random records
        MAX_RECORDS = 10

        # populate the database with fake customer records (assuming database was already cleared)
        try:
            fake = Faker()
            for _ in range(MAX_RECORDS):
                customer = Customer(
                    fullname=fake.name(),
                    mobile_no=f"07{fake.msisdn()[3:11]}",
                    address=fake.address(),
                    city=fake.city(),
                    email=fake.ascii_free_email(),
                )
                db.session.add(customer)
            del fake
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to fill database with customer records",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # populate staff records
        try:
            fake = Faker()
            staffRoles = [e.value for e in enums.StaffRole]
            for _ in range(MAX_RECORDS):
                member = Staff(
                    fullname=fake.name(),
                    role=random.choice(staffRoles),
                    mobile_no=f"07{fake.msisdn()[3:11]}",
                    email=fake.ascii_free_email(),
                )
                db.session.add(member)
            del fake
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to fill database with staff records",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # populate product records
        try:
            fake = Faker()
            product_categories = list(product_names.keys())
            for category in product_categories:
                for product_name, product_description in zip(
                    product_names[category], product_descriptions[category]
                ):
                    product = Product(
                        name=product_name,
                        description=product_description,
                        price=random.randrange(500, 2500, 10),
                        category=category,
                    )
                    db.session.add(product)
            del fake
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to fill database with products",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # commit changes to database
        try:
            db.session.commit()
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to commit changes to database",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # otherwise, return success JSON
        return generate_response(
            status_code=200,
            message="Successfully filled database",
            action="You have now populated the database with generic customers, staff and products",
            data={"flag": True},
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "username" in session:
            return redirect("/menu")
        return render_template("login.html", version=app.config.get("VERSION"))
    else:
        # clear session
        session.clear()

        # validate the presence of username and password attributes in payload
        response = validate_attributes(request.json, ["username", "password"])
        if response.status_code != 200:
            return response

        # otherwise, get username from database + save to session variable
        try:
            user = db.session.scalar(
                db.select(User).where(User.username == request.json["username"])
            )
        except:
            return generate_response(
                status_code=404,
                message="Username not found",
                action="Please register your account via an administrator",
                data={"flag": False},
            )

        # save user details in session cookie
        session["username"] = request.json["username"]
        session["password"] = request.json["password"]
        session["user_type"] = user.role.value
        session["fullname"] = user.fullname

        # verify password against saved password
        if not check_password_hash(user.password, request.json["password"]):
            return generate_response(
                status_code=401,
                message="Authentication failed",
                action="Incorrect password, please try again",
                data={"flag": False},
            )

        # return success JSON
        return generate_response(
            status_code=200,
            message="Login successful",
            action=f"You are now logged into FlamesPOS as '{request.json['username']}'",
            data={"flag": True},
        )


@app.route("/menu", methods=["GET", "POST"])
@login_required
def menu():
    if request.method == "GET":
        return render_template(
            "menu.html",
            version=app.config.get("VERSION"),
            fullname=session["fullname"].split(" ")[-1],
            quote=get_random_quote(),
            user_type=session["user_type"].title(),
        )


@app.route("/billing", methods=["GET", "POST"])
@login_required
def billing():
    if request.method == "GET":
        # get product category names
        try:
            categories = db.session.scalars(
                db.select(Product.category).distinct()
            ).all()
            category_list = ["All"] + [e.value.title() for e in categories]
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to get product categories",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # get full product details
        try:
            products = db.session.scalars(db.select(Product)).all()
            products_list = []
            for product in products:
                products_list.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "description": product.description,
                        "price": float(product.price),
                        "category_id": category_list.index(
                            product.category.value.title()
                        ),
                    }
                )
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to get all product details",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )
        
        # get list of pending orders
        try:
            pending_orders = db.session.scalars(
                db.select(Order.id).where(Order.status == enums.OrderStatus.pending)
            ).all()
        except:
            return generate_response(
                status_code=404,
                message="Pending orders not found",
                action="Please logout and login, and try again",
                data={"flag": False},
            )
        

        # if successful, get item and total lists for each pending order
        try:
            pass
            # for order_id in pending_orders:
            #     item_list = db.session.scalars(
            #         db.select(Product, OrderProduct).join_from(Product, OrderProduct).options(where(Product.orders.any(OrderProduct.order_id == order_id))
            #     ).all()
            #     print(item_list)
        except Exception as e:
            print(e)
            return generate_response(
                status_code=404,
                message="Could not create item list for pending orders",
                action="Please logout and login, and try again",
                data={"flag": False},
            )
        
        return render_template(
            "billing.html",
            version=app.config.get("VERSION"),
            categories=category_list,
            products=products_list,
        )


# note: /save_order route is NOT PUBLICLY visible
@app.route("/save_order", methods=["POST"])
@login_required
def saveOrder():
    if request.method == "POST":
        # verify the provided order data
        response = validate_attributes(
            request.json,
            ["totals", "items"],
        )
        if response.status_code != 200:
            return response

        # get the initiating user's id
        try:
            user_id = db.session.scalar(
                db.select(User.id).where(User.username == session["username"])
            )
        except:
            return generate_response(
                status_code=404,
                message="Username is invalid",
                action="This bill's creator is an invalid user, please logout and login again.",
                data={"flag": False},
            )

        # if successful, insert payment data w/ ptype="pending"
        # NOTE: paid and balance amounts will ONLY BE UPDATED upon confirming the payment
        # TODO: social_contrib_levy field must be changed depending on customer's requirements
        try:
            payment = Payment(
                subtotal=request.json["totals"]["subtotal"],
                paid=0,
                balance=0,
                discount=request.json["totals"]["discount"],
                service_charge=request.json["totals"]["service_charge"],
                value_added_tax=request.json["totals"]["value_added_tax"],
                social_contrib_levy=0,
                delivery_charge=request.json["totals"]["delivery_charge"],
                total=request.json["totals"]["total"],
            )
            db.session.add(payment)
            db.session.commit()
            payment_id = payment.id
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to add payment information",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # if successful, insert order data
        # NOTE: all orders are of otype="unconfirmed" when saved
        # NOTE: all orders are of status="pending" when saved
        # TODO: all orders are currently made by customer_id=1, please change it before distribution
        # TODO: all orders are currently assigned to staff_id=1, please change it before distribution
        try:
            order = Order(
                customer_id=1, user_id=user_id, payment_id=payment_id, staff_id=1
            )
            db.session.add(order)
            db.session.commit()
            order_id = order.id
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to add order information",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # if successful, insert order-product data
        try:
            for item_id in request.json["items"]:
                order_product = OrderProduct(
                    order_id=order_id,
                    product_id=item_id,
                    quantity=request.json["items"][item_id]["quantity"],
                )
                db.session.add(order_product)
            db.session.commit()
        except Exception as e:
            error = str(e)[: app.config.get("MAX_ERROR_LENGTH")] + " (more)"
            return generate_response(
                status_code=400,
                message="Failed to register order & payment information",
                action=f"Server responded with error: {error}",
                data={"flag": False},
            )

        # otherwise, return success JSON
        return generate_response(
            status_code=200,
            message="Successfully added order",
            action=f"You have now added order #{order_id} - you should see it on the pending list",
            data={
                "flag": True,
                "order_id": order_id
            },
        )


if __name__ == "__main__":
    app.run(debug=True, port=3000)

# Food-delivery-bot
Telegram bot that handles food delivery

#####################################################

BOT LOOP

/start

registration-number

show menu

get order

get location,name

recieve and verify payment

send to staff and drivers

######################################################

We have 4 roles
1.Customer
2.Admin (business owner)
3.Kitchen Staff
4.Driver

SYSTEM TYPE

Single Telegram Bot
Multiple role-based interfaces

The bot behaves differently depending on the user’s role.

Roles are identified by telegram_id.

Each role sees a different interface and different buttons.

ROLE DEFINITIONS

ROLE 1: CUSTOMER
Purpose: Place orders.

ROLE 2: ADMIN
Purpose: Manage orders and coordinate operations.

ROLE 3: KITCHEN
Purpose: See confirmed food preparation list.

ROLE 4: DRIVER
Purpose: See delivery assignments.

CUSTOMER SIDE (USER INTERFACE)

Customer can:

Start bot
View today's menu
Add items to cart
Checkout
Enter delivery info
Confirm payment
Track order status

ADMIN SIDE

Admin can:

Add / edit menu
Open / close orders
View all active orders
Verify payments
Confirm orders
Cancel orders
Send order to kitchen
Assign driver
View daily summary
Broadcast message to customers

KITCHEN SIDE

Kitchen role is simple and focused.

Kitchen can:

View confirmed orders only
View aggregated preparation summary
Mark order as "Prepared"

Kitchen does NOT:

See payments
See customer phone numbers (optional decision)
Edit menu
Cancel orders

Kitchen interface shows:

View 1:
"Today's Preparation Summary"

Item A – quantity
Item B – quantity

View 2:
Individual confirmed orders

Order ID
Items
Notes

When kitchen marks an order prepared:

Status updates
Admin gets notified

DRIVER SIDE

View assigned deliveries
See:
Customer name
Phone number
Location
Items
Mark order as:
Picked Up
Delivered

ORDER FLOW BETWEEN ROLES

Customer → creates order
Order status: Awaiting Payment

Admin → verifies payment
Order status: Confirmed

Admin → sends order to Kitchen
Kitchen sees it

Kitchen → marks Prepared
Admin notified

Admin → assigns to Driver
Driver sees delivery

Driver → marks Delivered
Order completed

That is the full operational loop.


STRUCTURE
One bot, role-based interface


PROJECT: Telegram Food Delivery Bot (aiogram)
STATUS: from registration to assign driver done
NEXT STEP: BUILD INTERFACES FOR ADMIN KITCHEN AND ADMIN
ARCHITECTURE DECISIONS: single kitchen, role-based system planned,SQlite
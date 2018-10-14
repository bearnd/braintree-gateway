# coding=utf-8

import marshmallow.validate


class SchemaSubscription(marshmallow.Schema):
    """Braintree subscription schema."""

    subscription_id = marshmallow.fields.String(
        required=True,
        dump_to="id",
        load_from="id",
        attribute="id",
        description=("The string value representing a specific subscription "
                     "in the Vault.")
    )

    plan_id = marshmallow.fields.String(
        required=True,
        description="The plan identifier.",
    )

    status = marshmallow.fields.String(
        required=True,
        validate=marshmallow.validate.OneOf(choices=[
            "Active",
            "Canceled",
            "Expired",
            "Past Due",
            "Pending",
        ])
    )

    price = marshmallow.fields.Decimal(
        required=False,
        as_string=True,
        description="The base price specified for a subscription.",
    )

    balance = marshmallow.fields.Decimal(
        required=False,
        as_string=True,
        description=("The amount of outstanding charges associated with a"
                     " subscription.")
    )

    billing_day_of_month = marshmallow.fields.Integer(
        required=False,
        description=("The value that specifies the day of the month that the "
                     "gateway will charge the subscription on every billing "
                     "cycle.")
    )

    current_billing_cycle = marshmallow.fields.Integer(
        required=True,
        description=("The subscription's current billing cycle. It is "
                     "incremented each time the subscription passes the"
                     " billing_period_end_date"),
    )

    days_past_due = marshmallow.fields.Integer(
        required=True,
        description="The number of days that the subscription is past due.",
    )

    payment_method_token = marshmallow.fields.String(
        required=True,
        description=("An alphanumeric value that references a specific payment"
                     "method stored in your Vault."),
    )

    trial_duration = marshmallow.fields.Integer(
        required=True,
        description="The trial timeframe specified in a plan.",
    )

    trial_duration_unit = marshmallow.fields.String(
        required=True,
        description=("The trial unit specified in a plan. Specify day or "
                     "month. Specifying a trial duration unit via the API "
                     "will override the subscription's plan details."),
    )

    trial_period = marshmallow.fields.Boolean(
        required=True,
        description=("A value indicating whether a subscription should begin "
                     "with a trial period. Specifying a trial period via the "
                     "API will override the subscription's plan details."),
    )

    created_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was created."
    )

    updated_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was last updated.",
    )

    class Meta:
        strict = True


class SchemaCreditCard(marshmallow.Schema):
    """ Braintree credit-card schema."""

    card_type = marshmallow.fields.String(
        required=True,
        validate=marshmallow.validate.OneOf(choices=[
            "American Express",
            "Carte Blanche",
            "China UnionPay",
            "Discover",
            "Elo",
            "JCB",
            "Laser",
            "Maestro",
            "MasterCard",
            "Solo",
            "Switch",
            "Visa",
            "Unknown",
        ]),
        description="The type of the credit card",

    )

    cardholder_name = marshmallow.fields.String(
        required=False,
        description="The cardholder name associated with the credit card."
    )

    customer_id = marshmallow.fields.String(
        required=True,
        description=("A string value representing an existing customer in your "
                     "Vault that owns this payment method.")
    )

    default = marshmallow.fields.Boolean(
        required=False,
        description="Whether the card is the default for the customer.",
    )

    expiration_month = marshmallow.fields.String(
        required=False,
        description="The expiration month of a credit card, formatted MM.",
    )

    expiration_year = marshmallow.fields.String(
        required=False,
        description=("The two or four digit year associated with a credit "
                     "card, formatted YYYY or YY."),
    )

    expired = marshmallow.fields.Boolean(
        required=False,
        description="Whether the card is expired.",
    )

    image_url = marshmallow.fields.String(
        required=False,
        description=("A URL that points to a payment method image resource "
                     "(a PNG file) hosted by Braintree."),
    )

    last_4 = marshmallow.fields.String(
        required=True,
        description="The last 4 digits of the credit card number.",
    )

    masked_number = marshmallow.fields.String(
        required=True,
        description=("A value comprising the bank identification number (BIN)"
                     ", 6 asterisks blocking out the middle numbers "
                     "(regardless of the number of digits present), and the "
                     "last 4 digits of the card number. This complies with PCI "
                     "security standards.")
    )

    subscriptions = marshmallow.fields.Nested(
        SchemaSubscription,
        many=True,
        required=False,
        description=("Subscriptions associated with the payment method, "
                     "sorted by creation date with the most recent last."),
    )

    token = marshmallow.fields.String(
        required=True,
        description=("An alphanumeric value that references a specific "
                     "payment method stored in your Vault."),
    )

    created_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was created."
    )

    updated_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was last updated.",
    )


class SchemaPayPalAccount(marshmallow.Schema):
    """ Braintree PayPal-account schema."""

    billing_agreement_id = marshmallow.fields.String(
        required=True,
        description=("The unique identifier of the vaulted payment flow "
                     "agreement between the customer's PayPal account and "
                     "your PayPal business account.")
    )

    customer_id = marshmallow.fields.String(
        required=True,
        description=("A string value representing an existing customer in your "
                     "Vault that owns this payment method.")
    )

    default = marshmallow.fields.Boolean(
        required=False,
        description=("A value indicating whether the specified payment "
                     "method is the default for the customer."),
    )

    email = marshmallow.fields.String(
        required=False,
        description=("The email address belonging to the PayPal account. This"
                     " field will not be populated if the PayPal transaction "
                     "declines and the payment method was not previously "
                     "stored in the Vault."),
    )

    image_url = marshmallow.fields.String(
        required=False,
        description=("A URL that points to a payment method image resource "
                     "(a PNG file) hosted by Braintree."),
    )

    payer_id = marshmallow.fields.String(
        required=True,
        description="The ID belonging to the PayPal account.",
    )

    subscriptions = marshmallow.fields.Nested(
        SchemaSubscription,
        many=True,
        required=False,
        description=("Subscriptions associated with the payment method, "
                     "sorted by creation date with the most recent last."),
    )

    created_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was created."
    )

    updated_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was last updated.",
    )


class SchemaCustomer(marshmallow.Schema):
    """ Braintree customer schema."""

    customer_id = marshmallow.fields.String(
        required=True,
        dump_to="id",
        load_from="id",
        attribute="id",
        description=("A string value representing this specific customer in "
                     "your Vault.")
    )

    first_name = marshmallow.fields.String(
        required=False,
        description="The first name.",
    )

    last_name = marshmallow.fields.String(
        required=False,
        description="The last name.",
    )

    email = marshmallow.fields.String(
        required=True,
        description="Email address composed of ASCII characters.",
    )

    phone = marshmallow.fields.String(
        required=False,
        description="Phone number.",
    )

    credit_cards = marshmallow.fields.Nested(
        SchemaCreditCard,
        many=True,
        required=False,
        description="Credit cards associated with the customer.",
    )

    paypal_accounts = marshmallow.fields.Nested(
        SchemaPayPalAccount,
        many=True,
        required=False,
        description="PayPal accounts associated with the customer.",
    )

    created_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was created."
    )

    updated_at = marshmallow.fields.DateTime(
        required=False,
        description="The date/time the object was last updated.",
    )

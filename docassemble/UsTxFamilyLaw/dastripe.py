import stripe
import json
import re
from docassemble.base.util import word, get_config, action_argument, DAObject, prevent_going_back
from docassemble.base.standardformatter import BUTTON_STYLE, BUTTON_CLASS
from docassemble.base.util import user_info

stripe.api_key = get_config('stripe secret key')

__all__ = ['DAStripe']

def truncate_price(price: float) -> float:
  """
  Truncate a price to two decimals. This is not rounding.
  """
  return float(int(price * 100)) / 100


class DAStripe(DAObject):
  def init(self, *pargs, **kwargs):
    if get_config('stripe public key') is None or get_config('stripe secret key') is None:
      raise Exception("In order to use a DAStripe object, you need to set stripe public key and stripe secret key in your Configuration.")
    super().init(*pargs, **kwargs)
    if not hasattr(self, 'button_label'):
      self.button_label = "Pay"
    if not hasattr(self, 'button_color'):
      self.button_color = "primary"
    if not hasattr(self, 'error_message'):
      self.error_message = "Please try another payment method."
    if hasattr(self, 'amount'):
      list_price = amount
      self.amount = self.discounted_price()
    self.is_setup = False

  def discounted_price(self):
    list_price = float(self.amount)
    currency = str(self.currency)
    discount_amount, discount_type = self.get_discount()
    discount_price = self.apply_discount(list_price, discount_amount, discount_type)
    
    if discount_price < .25:
      discount_price = 0.0
      self.amount = 0.0
      self.is_setup = True  # prevent creating an intent
      self.payment_successful = True  # force self.paid to be True
      self.result = {'payment_successful': True}

    return discount_price

  def apply_discount(self, list_price: float, discount_amount: int, discount_type: str) -> float:
    if discount_type not in ['$', '%']:
      return list_price
    if discount_amount < 0:
      return list_price

    if discount_type == '$':
      discount_price = truncate_price(max(0, list_price - float(abs(discount_amount))))
      return discount_price

    if discount_type == '%':
      if discount_amount > 100:
        return list_price
      discount_price = truncate_price(list_price * (100.00 - float(discount_amount)) / 100.00)
      return discount_price

    return list_price # Should never get here.

  def get_discount(self):
    the_user_info = user_info()
    user_privs = the_user_info.privileges
    for privilege in user_privs:
      discount_amount, discount_type = self.parse_discount(privilege)
      if discount_amount:
        return discount_amount, discount_type
    return None, None

  def parse_discount(self, privilege):
    """
    Parse the discount amount applicable to the current privilege.
    Discounts are indicated by docassemble user privileges having the
    form "DISCOUNT-(amount)(type)" where (amount) is the amount of the
    discount and (type) is either '$" or "%", indicating a fixed dollar
    amount to apply or a percentage to apply.

    The calling code will be responsible for sanitizing this (making sure,
    we don't have discounts that exceed 100% or negative dollar amounts.

    Params:
      privilege (str): The privilege to check

    Returns:
      Tuple: (amount to discount), (type, either "$" or "%")
      None: No discount detected.
    """
    match = re.match(r'DISCOUNT-(\d+)([%$])', privilege)
    if match:
      try:
        value = int(match.group(1))
      except:
        return None, None
      discount_type = match.group(2)
      return value, discount_type
    return None, None

  def setup(self):
    float(self.amount)
    str(self.currency)
    customer_id = self.get_customer_id()
    if self.amount > 0.0:
      self.intent = stripe.PaymentIntent.create(
        amount=int(float('%.2f' % float(self.amount))*100.0),
        currency=str(self.currency),
        statement_descriptor_suffix=self.description[:22],
        description=self.description,
        customer=customer_id,
        automatic_payment_methods={"enabled": True, "allow_redirects": "never"}  # Our flow won't work properly if we allow redirects
      )
    self.is_setup = True

  def get_customer_id(self) -> str:
    """
    Return the customer id of an eixsting customer. If the customer does not exist,
    then create a new customer and return the id of that new customer.

    Returns:
      str: Customer ID or blank if none found.
    """
    user_details = user_info()
    user_email = user_details.email
    self.payor.email = user_email
    result = stripe.Customer.search(query=f'email:"{user_email}"')
    customers = result.get('data', [])
    if not customers:
      customer = stripe.Customer.create(description=self.payor.description, email=user_email, name=str(self.payor))
    else:
      customer = customers[0]
    return customer.get('id', '')

  @property
  def html(self):
    if not self.is_setup:
      self.setup()
    return """\
<div id="stripe-payment-element" class="mt-2"></div>
<div id="stripe-errors" class="mt-2 mb-2 alert alert-danger" role="alert"></div>
<button class="btn """ + BUTTON_STYLE + self.button_color + " " + BUTTON_CLASS + '"' + """ id="stripe-submit">""" + word(self.button_label) + """</button>"""

  @property
  def javascript(self):
    if not self.is_setup:
      self.setup()
    billing_details = dict()
    try:
      billing_details['name'] = str(self.payor)
    except:
      pass
    address = dict()
    try:
      address['postal_code'] = self.payor.billing_address.zip
    except:
      pass
    try:
      address['line1'] = self.payor.billing_address.address
      address['line2'] = self.payor.billing_address.formatted_unit()
      address['city'] = self.payor.billing_address.city
      if hasattr(self.payor.billing_address, 'country'):
        address['country'] = address.billing_country
      else:
        address['country'] = 'US'
    except:
      pass
    if len(address):
      billing_details['address'] = address
    try:
      billing_details['email'] = self.payor.email
    except:
      pass
    try:
      billing_details['phone'] = self.payor.phone_number
    except:
      pass
    return """\
<script>
  const submitButton = document.getElementById('stripe-submit');

  const handleError = (error) => {
    const messageContainer = document.querySelector('#stripe-errors');
    messageContainer.textContent = error.message;
    submitButton.disabled = false;
  }

  var stripe = Stripe(""" + json.dumps(get_config('stripe public key')) + """);
  var client_secret = '""" + get_config('stripe secret key') + """'

  const payment_options = {
    layout: {
      type: 'accordion',
      defaultCollapsed: false,
      radios: false,
      spacedAccordionItems: true},
    business: {name: "JDBOT.US - MarriageDocs.Store"}
  };
  const elements_options = {
    mode: 'payment',
    amount: """ + str(self.intent.amount) + """,
    currency: '""" + self.intent.currency +"""',
    appearance: {theme: 'stripe'}
  }

  const elements = stripe.elements(elements_options);
  var card = elements.create('payment', payment_options);
  card.mount("#stripe-payment-element");

  card.addEventListener('change', ({error}) => {
    const displayError = document.getElementById('stripe-errors');
    if (error) {
      displayError.textContent = error.message;
    } else {
      displayError.textContent = '';
    }
  });

  submitButton.addEventListener('click', async (event) => {
  // We dont want to let default form submission happen here,
  // which would refresh the page.
  event.preventDefault();

  // Prevent multiple form submissions
  if (submitButton.disabled) {
    return;
  }

  // Disable form submission while loading
  submitButton.disabled = true;

  // Trigger form validation and wallet collection
  const {error: submitError} = await elements.submit();
  if (submitError) {
    handleError(submitError);
    return;
  }

  // Confirm the PaymentIntent using the details collected by the Payment Element
  const {error} = await stripe.confirmPayment({
    elements,
    clientSecret: '""" + self.intent.client_secret + """',
    confirmParams: {
      return_url: 'https://da.jdbot.us'
    },
    redirect: 'if_required'
  });

  if (error) {
    // This point is only reached if there's an immediate error when
    // confirming the payment. Show the error to your customer (for example, payment details incomplete)
    handleError(error);
  } else {
    // Your customer is redirected to your `return_url`. For some payment
    // methods like iDEAL, your customer is redirected to an intermediate
    // site first to authorize the payment, then redirected to the `return_url`.
    action_perform(""" + json.dumps(self.instanceName + '.success') + """, {result: {payment_successful: 1}});
  }
});
</script>
    """
  @property
  def paid(self):
    if not self.is_setup:
      self.setup()
    if hasattr(self, "payment_successful") and self.payment_successful:
      return True
    if not hasattr(self, 'result'):
      self.demand
    payment_status = stripe.PaymentIntent.retrieve(self.intent.id)
    if payment_status.amount_received == self.intent.amount:
      self.payment_successful = True
      return True
    return False

  def process(self):
    self.result = action_argument('result')
    self.paid
    prevent_going_back()

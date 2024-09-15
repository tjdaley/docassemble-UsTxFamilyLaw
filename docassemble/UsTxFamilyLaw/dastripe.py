import stripe
import json
from docassemble.base.util import word, get_config, action_argument, DAObject, prevent_going_back
from docassemble.base.standardformatter import BUTTON_STYLE, BUTTON_CLASS

stripe.api_key = get_config('stripe secret key')

__all__ = ['DAStripe']

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
    self.is_setup = False

  def setup(self):
    float(self.amount)
    str(self.currency)
    self.intent = stripe.PaymentIntent.create(
      amount=int(float('%.2f' % float(self.amount))*100.0),
      currency=str(self.currency),
    )
    self.is_setup = True

  @property
  def html(self):
    if not self.is_setup:
      self.setup()
    return """\
<div id="stripe-payment-element" class="mt-2"></div>
<div id="stripe-card-errors" class="mt-2 mb-2 text-alert" role="alert"></div>
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
    amount: """ + str(self.amount) + """,
    currency: 'usd',
    appearance: {theme: 'stripe'}
  }

  const elements = stripe.elements(elements_options);
  var card = elements.create('payment', payment_options);
  card.mount("#stripe-payment-element");

  card.addEventListener('change', ({error}) => {
    const displayError = document.getElementById('stripe-card-errors');
    if (error) {
      displayError.textContent = error.message;
    } else {
      displayError.textContent = '';
    }
  });
  var submitButton = document.getElementById('stripe-submit');
  submitButton.addEventListener('click', function(ev) {
    stripe.confirmCardPayment(""" + json.dumps(self.intent.client_secret) + """, {
      payment_method: {
        card: card,
        billing_details: """ + json.dumps(billing_details) + """
      }
    }).then(function(result) {
      if (result.error) {
        flash(result.error.message + "  " + """ + json.dumps(word(self.error_message)) + """, "danger");
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          action_perform(""" + json.dumps(self.instanceName + '.success') + """, {result: result})
        }
      }
    });
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

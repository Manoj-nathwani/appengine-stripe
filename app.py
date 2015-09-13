import os
import jinja2
import webapp2
import json
import stripe
import urllib2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({}))


class PostToStripe(webapp2.RequestHandler):
    def post(self):
        stripe.api_key = "sk_test_xxxxxxxxxxxxxxxxxx"
        token = self.request.get('stripeToken')
        try:
          charge = stripe.Charge.create(
              amount=1000, # amount in cents, again
              currency="gbp",
              source=token,
              description="Example charge"
          )
          self.response.write("Payment made, woo!")
        except stripe.error.CardError, e:
          self.response.write("The card has been declined")
          pass


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/PostToStripe', PostToStripe),
], debug=False)

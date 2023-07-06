def test_listing_contact_update_get(self):
    # Testing Anonymous User
    response = self.client.get(self.listing_contact_update)
    self.assertEqual(response.status_code, 302)

    # Testing Authenticated User
    self.client.login(email="test@gmail.com", password="Test@321")
    response = self.client.get(self.listing_contact_update)
    self.assertEqual(response.status_code, 403)

    # Testing Authenticated  Staff
    self.client.login(email="admin@gmail.com", password="Test@321")
    response = self.client.get(self.listing_contact_update)
    self.assertEqual(response.status_code, 200)


def test_listing_contact_update_post(self):
    # Testing Anonymous User
    response = self.client.post(self.listing_contact_update)
    self.assertEqual(response.status_code, 302)

    # Testing Authenticated User
    self.client.login(email="test@gmail.com", password="Test@321")
    response = self.client.post(self.listing_contact_update)
    self.assertEqual(response.status_code, 403)

    # Testing Authenticated  Staff
    self.client.login(email="admin@gmail.com", password="Test@321")
    response = self.client.post(self.listing_contact_update)
    self.assertEqual(response.status_code, 200)
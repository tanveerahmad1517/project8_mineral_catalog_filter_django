from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Mineral


class MineralViewTests(TestCase):
    def setUp(self):
        self.mineral1 = Mineral.objects.create(
            name='abelsonite',
            color='red',
            category='organic',
        )
        self.mineral2 = Mineral.objects.create(
            name='mineral2',
            color='red',
            category='sulfate',
        )
        self.mineral3 = Mineral.objects.create(
            name='mineral3',
            color='transparent',
            category='nitrate',
        )

    def test_mineral_list_view(self):
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral1, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral1.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_list_view_filter_by_color(self):
        url = reverse('minerals:list') + '?color=red'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral1, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertNotIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral1.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_list_view_by_other_color(self):
        url = reverse('minerals:list') + '?color=other'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral1, resp.context['minerals'])
        self.assertNotIn(self.mineral2, resp.context['minerals'])
        self.assertIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral3.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_list_view_filter_by_category(self):
        url = reverse('minerals:list') + '?category=organic'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral1, resp.context['minerals'])
        self.assertNotIn(self.mineral2, resp.context['minerals'])
        self.assertNotIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral1.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_list_view_by_other_category(self):
        url = reverse('minerals:list') + '?category=other'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral1, resp.context['minerals'])
        self.assertNotIn(self.mineral2, resp.context['minerals'])
        self.assertIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral3.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_list_view_first_letter(self):
        url = reverse('minerals:list') + '?first_letter=m'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral1, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral2.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_detail_view(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral1.name, resp.context['properties'].values())
        self.assertContains(resp, self.mineral1.name)
        self.assertTemplateUsed(resp, 'minerals/detail.html')
        self.assertEqual(self.mineral3.pk, resp.context['previous_id'])
        self.assertEqual(self.mineral2.pk, resp.context['next_id'])

        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral2.pk}))
        self.assertEqual(self.mineral3.pk, resp.context['next_id'])
        self.assertEqual(self.mineral1.pk, resp.context['previous_id'])

        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': self.mineral3.pk}))

        self.assertEqual(self.mineral1.pk, resp.context['next_id'])
        self.assertEqual(self.mineral2.pk, resp.context['previous_id'])

    def test_mineral_detail_view_404(self):
        resp = self.client.get(reverse('minerals:detail',
                                       kwargs={'pk': 10}))
        self.assertEqual(resp.status_code, 404)

    def test_mineral_search(self):
        url = reverse('minerals:search') + '?q=mineral'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral1, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertIn(self.mineral3, resp.context['minerals'])
        self.assertContains(resp, self.mineral3.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

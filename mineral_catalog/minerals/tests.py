from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Mineral


class MineralViewTests(TestCase):
    def setUp(self):
        self.mineral = Mineral.objects.create(
            name='mineral'
        )
        self.mineral2 = Mineral.objects.create(
            name='mineral2'
        )

    def test_mineral_list_view(self):
        resp = self.client.get(reverse('minerals:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertContains(resp, self.mineral.name)
        self.assertTemplateUsed(resp, 'minerals/index.html')

    def test_mineral_detail_view(self):
        resp = self.client.get(reverse('minerals:detail', kwargs={'pk': self.mineral.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral.name, resp.context['properties'].values())
        self.assertContains(resp, self.mineral.name)
        self.assertTemplateUsed(resp, 'minerals/detail.html')

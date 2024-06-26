from unittest import TestCase
from utils.pagination import make_pagination_range
from django.urls import reverse
from django.test import TestCase


class TestPagination(TestCase):
    def test_make_pagination_range_return_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1,2,3,4], pagination['pagination'])
        
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1,2,3,4], pagination['pagination'])
        
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertEqual([1,2,3,4], pagination['pagination'])
                
        
    def test_make_sure_middle_ranges_are_correct(self):      
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=3,
        )
        self.assertEqual([2,3,4,5], pagination['pagination'])
        
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=4,
        )
        self.assertEqual([3,4,5,6], pagination['pagination'])
        
    def test_make_paginations_stops_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=18,
        )
        self.assertEqual([17,18,19,20], pagination['pagination'])
        
        pagination = make_pagination_range(
            page_range=list(range(1,21)),
            qty_pages=4,
            current_page=19,
        )
        self.assertEqual([17,18,19,20], pagination['pagination'])
        
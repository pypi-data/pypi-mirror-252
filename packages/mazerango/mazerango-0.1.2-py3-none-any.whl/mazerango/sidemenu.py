# -*- coding: utf-8 -*-
SIDEMENU_SETTING = [
    {
        'name':
            '사이트 관리',
        'links': [
            {
                'name': '사이트',
                'url': '/admin/company/site',
                'icon': 'fas fa-tv',
                'permissions': ['company.view_site']
            },
            {
                'name': '블랙리스트',
                'url': '/admin/entry/blacklist',
                'icon': 'fas fa-list',
                'permissions': ['entry.view_blacklist'],
            },
        ]
    },
    {
        'name':
            '캠페인 관리',
        'links': [
            {
                'name': '캠페인',
                'url': '/admin/campaign/campaign',
                'icon': 'fas fa-bullhorn',
                'permissions': ['campaign.view_campaign']
            },
        ],
    },
    {
        'name':
            '액션 모듈 관리',
        'links': [
            {
                "name": "액션 모듈 설정",
                "url": "/admin/module/campaignmodule",
                "icon": "fas fa-cogs",
                "permissions": ["campaign.view_campaignmodule"],
            },
            {
                'name': '개인정보',
                'url': '/admin/module/privacy',
                'icon': 'fas fa-user-shield',
                'permissions': ['module.view_privacy']
            },
            {
                'name': '상품',
                'url': '/admin/module/reward',
                'icon': 'fas fa-gift',
                'permissions': ['module.view_reward'],
            },
            {
                'name': '선택형 상품',
                'url': '/admin/module/rewardoptional',
                'icon': 'fas fa-gift',
                'permissions': ['module.view_rewardoptional'],
            },
            {
                'name': '설문',
                'url': '/admin/module/survey',
                'icon': 'fas fa-poll',
                'permissions': ['module.view_survey'],
            },
            {
                'name': '리뷰',
                'url': '/admin/module/review',
                'icon': 'fas fa-comments',
                'permissions': ['module.view_review'],
            },
        ]
    },
    {
        'name':
            '캠페인 참여자 관리',
        'links': [
            {
                'name': '참여자',
                'url': '/admin/entry/entry',
                'icon': 'fas fa-file-alt',
                'permissions': ['entry.view_entry']
            },
            {
                'name': '당첨자',
                'url': '/admin/raffle/winner',
                'icon': 'fas fa-file-alt',
                'permissions': ['raffle.view_winner']
            },
        ]
    },
    {
        'name':
            '운영사 관리',
        'links': [
            {
                'name': '운영사',
                'url': '/admin/company/company',
                'icon': 'fas fa-building',
                'permissions': ['company.view_company']
            },
            {
                'name': '임직원',
                'url': '/admin/company/staffmanage',
                'icon': 'fas fa-user',
                'permissions': ['company.view_staffmanage']
            },
        ]
    },
    {
        'name':
            '사용자 관리',
        'links': [
            {
                'name': '사용자',
                'url': '/admin/siteuser/siteuser',
                'icon': 'fas fa-user',
                'permissions': ['siteuser.view_siteuser']
            },
        ]
    },
]

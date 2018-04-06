virgo = {
    'build': {
        '__attrs_files': ['file'],
        ':id': {
            'log': {}
        }
    }
}
ruote = {
    'AWSclusters': {
        ':id': {
            'stop_cluster': {},
            'resume_cluster': {}
        }
    },
    'AzureClusters': {
        ':id': {}
    },
    'apps': {
        ':id': {
            'additional': {
                ':id': {}
            },
            'check_container': {},
            'log': {},
            'ranking': {},
            'settings': {
                ':id': {}
            },
            'stats': {}
        },
        'build': {},
        'finishbuild': {},
        'setting_attributes': {}
    },
    'clusters': {
        ':id': {
            'check': {},
            'stats': {},
            'update_details': {},
            'libraries': {
                ':id': {}
            },
            'metadata': {
                ':id': {}
            }
        }
    },
    'datasets': {
        ':id': {}
    },
    'files': {
        '__attrs_files': ['file'],
        ':id': {
            'download': {},
            'upload': {}
        }
    },
    'jobs': {
        ':id': {
            'cancel': {},
            'check_threshold': {},
            'stdout': {},
            'stderr': {},
            'logtarball': {},
            'log': {},
            'perf': {},
            'telemetry': {}
        }
    },
    'queues': {
        'metadata_attributes': {},
        ':id': {
            'statistics': {},
            'stats': {},
            'metadata': {
                ':id': {}
            }
        }
    },
    'users': {
        'me': {
            'stats': {},
        },
        ':id': {
            'stats': {},
        }
    },
    'vdcs': {
        ':id': {
            'stats': {},
        }
    },
    'update_job': {},
    'sso': {
        'token_by_email': {},
        'providers': {},
    },
    'jobs-by-uuid': {
        ':uuid': {
            'query': {},
        }
    }
}

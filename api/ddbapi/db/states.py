states = [
    'NOT_STARTED',
    'STARTED',
    'IN_PROGRESS',
    'COMPLETED',
    'STOPPED',
    'ERROR'
]

allowed_transitions = {
    'NOT_STARTED': ['STARTED', 'ERROR'],
    'STARTED': ['IN_PROGRESS', 'ERROR'],
    'IN_PROGRESS': ['COMPLETED', 'STOPPED', 'ERROR'],
    'COMPLETED': ['NOT_STARTED'],
    'STOPPED': ['ERROR', 'NOT_STARTED' 'STARTED'],
    'ERROR': ['STOPPED'],
}
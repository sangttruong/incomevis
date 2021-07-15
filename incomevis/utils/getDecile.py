def getDecile(type):
    if type == 'numeric': [0.05, 0.15, 0.25, 0.35, 0.45, 0.50, 0.55, 0.65, 0.75, 0.85, 0.95]
    elif type == 'string': return ['5p','15p','25p','35p','45p','50p','55p','65p','75p','85p','95p']
    else: raise ValueError
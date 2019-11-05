# --------------------------------------------------
#
# Options are loaded from a configuration file
#
# --------------------------------------------------


def load_options(user_config):
    """
    map options from user input into the default config
    """
    sections = user_config.sections()

    for s in sections:
        options = user_config.options(s)

    # --------------------------------------------------
    # options
    # --------------------------------------------------
    options = {}

    # experiment name (where trained weights are)
    # options['experiment'] = user_config.get('model', 'name')
    #options['train_folder'] = user_config.get('database', 'train_folder')
    options['datasets'] = user_config.get('database', 'datasets_folder')
    options['output_folder'] = '/output'
    options['current_scan'] = 'scan'
    #options['t1_name'] = user_config.get('database', 't1_name')
    #options['flair_name'] = user_config.get('database', 'flair_name')
    options['flair_tags'] = [el.strip() for el in
                             user_config.get('database',
                                                'flair_tags').split(',')]
    options['t1_tags'] = [el.strip() for el in
                          user_config.get('database',
                                             't1_tags').split(',')]
    options['t2_tags'] = [el.strip() for el in
                            user_config.get('database',
                                               't2_tags').split(',')]
    options['mod4_tags'] = [el.strip() for el in
                            user_config.get('database',
                                               'mod4_tags').split(',')]
    options['mask_tags'] = [el.strip() for el in
                           user_config.get('database',
                                              'mask_tags').split(',')]
    # options['ROI_name'] = user_config.get('database', 'ROI_name')
    options['debug'] = user_config.get('database', 'debug')

    # modalities = [str(options['flair_tags'][0]),
    #               options['t1_tags'][0],
    #               options['t2_tags'][0],
    #               options['mod4_tags'][0]]
    # names = ['FLAIR', 'T1', 'T2', 'MOD4']

    # options['modalities'] = [n for n, m in
    #                          zip(names, modalities) if m != 'None']
    #options['image_tags'] = [m for m in modalities if m != 'None']
    # options['x_names'] = [n + '_brain.nii.gz' for n, m in
    #                       zip(names, modalities) if m != 'None']

    options['out_name'] = 'out_seg.nii.gz'

    # preprocessing
    options['register_modalities'] = (user_config.get('database',
                                                         'register_modalities'))
    options['denoise'] = (user_config.get('database',
                                             'denoise'))
    options['denoise_iter'] = (user_config.getint('database',
                                                     'denoise_iter'))
    options['skull_stripping'] = (user_config.get('database',
                                                     'skull_stripping'))
    options['save_tmp'] = (user_config.get('database', 'save_tmp'))

      
    options = parse_values_to_types(options)
    return options


def parse_values_to_types(options):
    """
    process values into types
    """

    keys = options.keys()
    for k in keys:
        value = options[k]
        if value == 'True':
            options[k] = True
        if value == 'False':
            options[k] = False

    return options


def print_options(options):
    """
    print options
    """
    print "--------------------------------------------------"
    print " configuration options:"
    print "--------------------------------------------------"
    print " "
    keys = options.keys()
    for k in keys:
        print k, ':', options[k]
    print "--------------------------------------------------"

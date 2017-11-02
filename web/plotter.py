import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from helpers import timeit
import numpy as np
import seaborn as sns
import json
import numpy as np
np.set_printoptions(precision=3)


@timeit
def plot(url, name_clean):
    j_name = './static/{}.json'.format(name_clean)

    json_results = json.load(open(j_name))
    results_ = {k: v for k, v in json_results[0].items()}

    # results_ = {
    #     "center": 0.245,
    #     "conspiracy": 0.219,
    #     "extremeleft": 0.211,
    #     "extremeright": 0.253,
    #     "fakenews": 0.269,
    #     "hate": 0.255,
    #     "high": 0.235,
    #     "left": 0.251,
    #     "left-center": 0.178,
    #     "low": 0.198,
    #     "mixed": 0.246,
    #     "pro-science": 0.326,
    #     "propaganda": 0.255,
    #     "right": 0.243,
    #     "right-center": 0.243,
    #     "veryhigh": 0.267
    # }

    def get_spectrum(spec, name, colors):
        spec = dict(zip(spec, range(len(spec))))
        y, x = list(
            zip(*sorted(filter(lambda kv: kv[0] in spec, results_.items()), key=lambda kv: spec[kv[0]])))
        y, x = list(zip(*sorted(denoise(x, y).items(), key=lambda kv: spec[kv[0]])))
        make_fig(x, y, name, colors)

    def denoise(x, y):
        xy = dict(zip(y, x))

        for key in xy:
            if key in noise_factor:
                xy[key] -= xy[key] * noise_factor[key]
                # xy[key] -= (xy[key] * (1 - noise_factor[key]))

                # xy[key] = xy[key] - (xy[key] * noise_factor[key] * 16)
                pass

        return xy

    sns.set(style='whitegrid', font='Tahoma', font_scale=1.7)

    def label_cleaner(y):
        key = {
            'fakenews': 'fake news',
            'extremeright': 'extreme right',
            'extremeleft': 'extreme left',
            'veryhigh': 'very high veracity',
            'low': 'low veracity',
            'pro-science': 'pro science',
            'mixed': 'mixed veracity',
            'high': 'high veracity'
        }
        for label in y:
            for k, v in key.items():
                if label == k:
                    label = v.title()

            yield label.title()

    noise_factor = {
        'hate': -0.8961313715119581,
        'low': 0.0,
        'propaganda': -0.92395924271485685,
        'conspiracy': -0.29321540314409578,
        'center': -0.63902146830732409,
        'pro-science': -0.61516991760605277,
        'veryhigh': -0.45272065711245246,
        'extremeright': -0.89521375908850598,
        'mixed': -0.86550605687922566,
        'right-center': -0.66138189882048526,
        'extremeleft': -0.33568683927126164,
        'high': -0.7514481071057596,
        'right': -0.90024788280050327,
        'left-center': -0.27028146486627702,
        'left': -0.74069802267267471,
        'fakenews': -1.0
    }
    s = sum(noise_factor.values())
    noise_factor = {k: v / s for k, v in noise_factor.items()}
    default_cp = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    policic_colors = ["#9c3229", "#C8493A", "#D6837F", "#DCDDDD", "#98B5C6", "#6398C9", "#3F76BB"]
    veracity_colors = ["#444784", "#2F7589", "#29A181", "#7CCB58"]
    charachter_colors = ["#444784", "#7CCB58", "#3976C5", "#02B97C", "#C8493A"]

    def make_fig(x, y, cat, colors='coolwarm_r'):
        color_p = default_cp
        if cat == "Political":
            color_p = policic_colors
        elif cat == "Accuracy":
            color_p = veracity_colors
        elif cat == "Character":
            color_p = charachter_colors

        y = list(label_cleaner(y))

        plt.figure(figsize=(8, 8))
        y_pos = np.arange(len(y))
        # x = np.square(np.asarray(x))
        x = np.asarray(x)
        print(dict(zip(y, x.round(4).astype(str))))
        g = sns.barplot(y=y_pos, x=x, palette=(sns.color_palette(color_p)), orient='h', saturation=.9)
        plt.yticks(y_pos, y)
        plt.title('{} - {}'.format(url, cat))
        plt.xlabel('Text similarity')
        plt.xlim(0, .5)
        # frame1 = plt.gca()
        # frame1.axes.xaxis.set_ticklabels([])
        plt.savefig(
            './static/{}.png'.format(name_clean + '_' + cat), format='png', bbox_inches='tight', dpi=100)

        plt.clf()

    get_spectrum(
        ['extremeright', 'right', 'right-center', 'center', 'left-center', 'left',
         'extremeleft'], 'Political', 'policic_colors')

    get_spectrum(['veryhigh', 'high', 'mixed', 'low', 'unreliable'], 'Accuracy', 'veracity_colors')
    plt.close('all')

    get_spectrum(['conspiracy', 'fakenews', 'propaganda', 'pro-science', 'hate'], 'Character',
                 'charachter_colors')


if __name__ == '__main__':

    plot(
        ' _test_',
        'infowarscom',)

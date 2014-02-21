# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Worldmap chart

"""

from __future__ import division
from pygal.ghost import ChartCollection
from pygal.util import cut, cached_property, decorate
from pygal.graph.graph import Graph
from pygal._compat import u
from numbers import Number
from lxml import etree
import os


DEPARTMENTS = {
    '01': u("Ain"),
    '02': u("Aisne"),
    '03': u("Allier"),
    '04': u("Alpes-de-Haute-Provence"),
    '05': u("Hautes-Alpes"),
    '06': u("Alpes-Maritimes"),
    '07': u("Ardèche"),
    '08': u("Ardennes"),
    '09': u("Ariège"),
    '10': u("Aube"),
    '11': u("Aude"),
    '12': u("Aveyron"),
    '13': u("Bouches-du-Rhône"),
    '14': u("Calvados"),
    '15': u("Cantal"),
    '16': u("Charente"),
    '17': u("Charente-Maritime"),
    '18': u("Cher"),
    '19': u("Corrèze"),
    '2A': u("Corse-du-Sud"),
    '2B': u("Haute-Corse"),
    '21': u("Côte-d'Or"),
    '22': u("Côtes-d'Armor"),
    '23': u("Creuse"),
    '24': u("Dordogne"),
    '25': u("Doubs"),
    '26': u("Drôme"),
    '27': u("Eure"),
    '28': u("Eure-et-Loir"),
    '29': u("Finistère"),
    '30': u("Gard"),
    '31': u("Haute-Garonne"),
    '32': u("Gers"),
    '33': u("Gironde"),
    '34': u("Hérault"),
    '35': u("Ille-et-Vilaine"),
    '36': u("Indre"),
    '37': u("Indre-et-Loire"),
    '38': u("Isère"),
    '39': u("Jura"),
    '40': u("Landes"),
    '41': u("Loir-et-Cher"),
    '42': u("Loire"),
    '43': u("Haute-Loire"),
    '44': u("Loire-Atlantique"),
    '45': u("Loiret"),
    '46': u("Lot"),
    '47': u("Lot-et-Garonne"),
    '48': u("Lozère"),
    '49': u("Maine-et-Loire"),
    '50': u("Manche"),
    '51': u("Marne"),
    '52': u("Haute-Marne"),
    '53': u("Mayenne"),
    '54': u("Meurthe-et-Moselle"),
    '55': u("Meuse"),
    '56': u("Morbihan"),
    '57': u("Moselle"),
    '58': u("Nièvre"),
    '59': u("Nord"),
    '60': u("Oise"),
    '61': u("Orne"),
    '62': u("Pas-de-Calais"),
    '63': u("Puy-de-Dôme"),
    '64': u("Pyrénées-Atlantiques"),
    '65': u("Hautes-Pyrénées"),
    '66': u("Pyrénées-Orientales"),
    '67': u("Bas-Rhin"),
    '68': u("Haut-Rhin"),
    '69': u("Rhône"),
    '70': u("Haute-Saône"),
    '71': u("Saône-et-Loire"),
    '72': u("Sarthe"),
    '73': u("Savoie"),
    '74': u("Haute-Savoie"),
    '75': u("Paris"),
    '76': u("Seine-Maritime"),
    '77': u("Seine-et-Marne"),
    '78': u("Yvelines"),
    '79': u("Deux-Sèvres"),
    '80': u("Somme"),
    '81': u("Tarn"),
    '82': u("Tarn-et-Garonne"),
    '83': u("Var"),
    '84': u("Vaucluse"),
    '85': u("Vendée"),
    '86': u("Vienne"),
    '87': u("Haute-Vienne"),
    '88': u("Vosges"),
    '89': u("Yonne"),
    '90': u("Territoire de Belfort"),
    '91': u("Essonne"),
    '92': u("Hauts-de-Seine"),
    '93': u("Seine-Saint-Denis"),
    '94': u("Val-de-Marne"),
    '95': u("Val-d'Oise"),
    '971': u("Guadeloupe"),
    '972': u("Martinique"),
    '973': u("Guyane"),
    '974': u("Réunion"),
    # Not a area anymore but in case of...
    '975': u("Saint Pierre et Miquelon"),
    '976': u("Mayotte")
}


REGIONS = {
    '11': u("Île-de-France"),
    '21': u("Champagne-Ardenne"),
    '22': u("Picardie"),
    '23': u("Haute-Normandie"),
    '24': u("Centre"),
    '25': u("Basse-Normandie"),
    '26': u("Bourgogne"),
    '31': u("Nord-Pas-de-Calais"),
    '41': u("Lorraine"),
    '42': u("Alsace"),
    '43': u("Franche-Comté"),
    '52': u("Pays-de-la-Loire"),
    '53': u("Bretagne"),
    '54': u("Poitou-Charentes"),
    '72': u("Aquitaine"),
    '73': u("Midi-Pyrénées"),
    '74': u("Limousin"),
    '82': u("Rhône-Alpes"),
    '83': u("Auvergne"),
    '91': u("Languedoc-Roussillon"),
    '93': u("Provence-Alpes-Côte d'Azur"),
    '94': u("Corse"),
    '01': u("Guadeloupe"),
    '02': u("Martinique"),
    '03': u("Guyane"),
    '04': u("Réunion"),
    # Not a region anymore but in case of...
    '05': u("Saint Pierre et Miquelon"),
    '06': u("Mayotte")
}


with open(os.path.join(
        os.path.dirname(__file__),
        'fr.departments.svg')) as file:
    DPT_MAP = file.read()


with open(os.path.join(
        os.path.dirname(__file__),
        'fr.regions.svg')) as file:
    REG_MAP = file.read()


class FrenchMapDepartments(Graph):
    """French department map"""
    _dual = True
    x_labels = list(DEPARTMENTS.keys())
    area_names = DEPARTMENTS
    area_prefix = 'z'
    svg_map = DPT_MAP


    @cached_property
    def _values(self):
        """Getter for series values (flattened)"""
        return [val[1]
                for serie in self.series
                for val in serie.values
                if val[1] is not None]

    def _plot(self):
        map = etree.fromstring(self.svg_map)
        map.set('width', str(self.view.width))
        map.set('height', str(self.view.height))

        for i, serie in enumerate(self.series):
            safe_vals = list(filter(
                lambda x: x is not None, cut(serie.values, 1)))
            if not safe_vals:
                continue
            min_ = min(safe_vals)
            max_ = max(safe_vals)
            for j, (area_code, value) in enumerate(serie.values):
                if isinstance(area_code, Number):
                    area_code = '%2d' % area_code
                if value is None:
                    continue
                if max_ == min_:
                    ratio = 1
                else:
                    ratio = .3 + .7 * (value - min_) / (max_ - min_)
                areae = map.xpath(
                    "//*[contains(concat(' ', normalize-space(@class), ' '),"
                    " ' %s%s ')]" % (self.area_prefix, area_code))
                if not areae:
                    continue
                for area in areae:
                    cls = area.get('class', '').split(' ')
                    cls.append('color-%d' % i)
                    area.set('class', ' '.join(cls))
                    area.set('style', 'fill-opacity: %f' % (ratio))

                    metadata = serie.metadata.get(j)
                    if metadata:
                        parent = area.getparent()
                        node = decorate(self.svg, area, metadata)
                        if node != area:
                            area.remove(node)
                            index = parent.index(area)
                            parent.remove(area)
                            node.append(area)
                            parent.insert(index, node)

                    last_node = len(area) > 0 and area[-1]
                    if last_node is not None and last_node.tag == 'title':
                        title_node = last_node
                        text = title_node.text + '\n'
                    else:
                        title_node = self.svg.node(area, 'title')
                        text = ''
                    title_node.text = text + '[%s] %s: %d' % (
                        serie.title,
                        self.area_names[area_code], value)

        self.nodes['plot'].append(map)


class FrenchMapRegions(FrenchMapDepartments):
    """French regions map"""
    x_labels = list(REGIONS.keys())
    area_names = REGIONS
    area_prefix = 'a'
    svg_map = REG_MAP


class FrenchMap(ChartCollection):
    Regions = FrenchMapRegions
    Departments = FrenchMapDepartments
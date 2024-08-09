#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dashboard-stats.py
#  
#  Copyright 2024 Santiago Banchero <santiago@CSCYAHIDRO081N>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import streamlit as st
import pandas as pd
import numpy as np
from glob import glob
from os.path import basename

files_csv = {
	"Argentina": {
		"LEVEL_1": "Areas-cover-col5-v2-arg-level_1-FINAL_join.csv",
		"LEVEL_2": "Areas-cover-col5-v2-arg-level_2-FINAL_join.csv",
		"LEVEL_3": "Areas-cover-col5-v2-arg-level_3-FINAL_join.csv",
	},
	"Bolivia": {
		"LEVEL_1": "Areas-cover-col5-v2-bol-level_1-FINAL_join.csv",
		"LEVEL_2": "Areas-cover-col5-v2-bol-level_2-FINAL_join.csv",
		"LEVEL_3": "Areas-cover-col5-v2-bol-level_3-FINAL_join.csv",
	},
	"Paraguay": {
		"LEVEL_1": "Areas-cover-col5-v2-par-level_1-FINAL_join.csv",
		"LEVEL_2": "Areas-cover-col5-v2-par-level_2-FINAL_join.csv",
		"LEVEL_3": "Areas-cover-col5-v2-par-level_3-FINAL_join.csv",
	}
}


data_dir = "./data/"

st.markdown("# Estadisticas MapBiomas Chaco")

def get_data(f):
	return pd.read_csv(f"{data_dir}{f}")

with st.sidebar:
	st.image(image="./images/logo.png", width=200)

	paises = list(files_csv.keys())
	opt_pais = st.selectbox(
		label="Pais",
		options=paises,
		placeholder="Seleccione una opción ..."
	)
	levels = list(files_csv[opt_pais].keys())

	opt_level = st.selectbox(
		label="Assets",
		options=levels,
		placeholder="Seleccione una opción ..."
	)
	
	df = pd.read_csv(f"{data_dir}{files_csv[opt_pais][opt_level]}")
	
	class_name = df["class_name"].unique().tolist()
	
	mult_opt_class = st.multiselect(
		label="Clases",
		options=class_name,
		placeholder="Seleccione una opción ...",
	)

	levels = df[opt_level].unique().tolist()
	
	mult_opt_levels = st.multiselect(
		label="Levels",
		options=levels,
		placeholder="Seleccione una opción ...",
	)

dfg = df[df["class_name"].isin(mult_opt_class) & df[opt_level].isin(mult_opt_levels)].groupby(['class_name', "year", opt_level], as_index=False)['area'].sum()
dfg

st.bar_chart(dfg, x="year", y="area", color="class_name", stack=False)

dfgs=dfg.sort_values(by=['year'])
dfgs["dif_area"] = dfgs["area"].diff().fillna(0)
dfgs["dif_area_porc"] = dfgs["dif_area"]/(dfgs["area"] + dfgs["dif_area"]) * 100
dfgs
st.bar_chart(dfgs, x="year", y="dif_area_porc", color="class_name", stack=False)



import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np


#with st.echo(code_location='below'):

	# Initial state
if "total_points" not in state:
	state.total_points = 2000
if "num_turns" not in state:
	state.num_turns = 9

total_points = st.slider("Number of points in spiral", None, 5000, 2000, key="total_points")
num_turns = st.slider("Number of turns in spiral", None, 100, 9, key="num_turns")

def set_num_turns(x=1):
	state.num_turns = x
def set_total_points(x=1):
	state.total_points = x

st.button("1 turn", on_click=set_num_turns)



@st.experimental_memo
def get_data(total_points, num_turns):

	with st.spinner("running get_data"):
		data = []
		points_per_turn = total_points / num_turns
		points = np.arange(total_points)
		curr_turn, i = np.divmod(points, points_per_turn)
		angle = (curr_turn + 1) * 2 * np.pi * i / points_per_turn
		radius = points / total_points
		x = radius * np.cos(angle)
		y = radius * np.sin(angle)

		data = pd.DataFrame(dict(x=x, y=y))
		
		# for curr_point_num in range(total_points):
		# 	curr_turn, i = divmod(curr_point_num, points_per_turn)
		# 	angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
		# 	radius = curr_point_num / total_points
		# 	x = radius * math.cos(angle)
		# 	y = radius * math.sin(angle)
		# 	data.append(dict(x=x, y=y))
		# data = pd.DataFrame(data)
	return data

@st.experimental_memo
def plot_spiral(total_points, num_turns):

	df = get_data(total_points, num_turns)

	with st.spinner("plotting plot_spiral"):
		st.altair_chart(alt.Chart(df, height=500, width=500)
			.mark_circle(color='#0068c9', opacity=0.5)
			.encode(x='x:Q', y='y:Q'))


@st.experimental_singleton
def cache_all():
	empty = st.empty()
	with st.spinner(f"caching all"):
		for i in range(1, 101):
			with empty:
				#st.write(f"{i} turn")
				plot_spiral(total_points, i)

cache_all()

st.write("Plot")
plot_spiral(total_points, num_turns)
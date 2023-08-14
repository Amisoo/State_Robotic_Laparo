import plotly.graph_objects as go
import pandas as pd
from get_title_file import get_title_graph
import numpy as np

def plot(arg):

    df = pd.read_csv(arg)



    timestamps_row = pd.to_datetime(df['timestamps']).tolist()

    timestamps_last_row = timestamps_row[-1]
    timestamps_first_row = timestamps_row[0]

    # total time
    total_duration = (pd.to_datetime(timestamps_last_row) - pd.to_datetime(timestamps_first_row)).total_seconds()

    # motion state 3 data
    # mask motion state 3
    mask = df['Motion_State'] == 3
    mask = mask.astype(int).diff()

    # start, end of motion state 3
    timestamps_start_motionstate = pd.to_datetime(df['timestamps'][mask == 1]).tolist()
    timestamps_end_motionstate = pd.to_datetime(df['timestamps'][mask == -1]).tolist()

    # condition if finish on state 3
    if len(timestamps_start_motionstate) > len(timestamps_end_motionstate):
        timestamps_end_motionstate.append(timestamps_last_row)

    total_time_state3 = sum((pd.to_datetime(timestamps_end_motionstate) - pd.to_datetime(timestamps_start_motionstate)).total_seconds())

    # perecentage of state3
    percentage_state3 = round(100 * (total_time_state3 / total_duration), 3)

    # laparo data

    mask = df['Main_Control_Current_Sub_State'] == 1365
    mask = mask.astype(int).diff()

    # start end of substate AtLaparo
    timestamps_start = pd.to_datetime(df['timestamps'][mask == 1]).tolist()
    timestamps_end = pd.to_datetime(df['timestamps'][mask == -1]).tolist()

    # condition if finish substate AtLaparo
    if len(timestamps_start) > len(timestamps_end):
        timestamps_end.append(timestamps_last_row)

    # total AtLaparo [s]
    total_duration_at_laparo = sum((pd.to_datetime(timestamps_end) - pd.to_datetime(timestamps_start)).total_seconds())

    # percentage substate AtLaparo
    percentage_at_laparo = round(100 * (total_duration_at_laparo / total_duration), 3)


    # Ready for operating

    mask = df['Device_State'] == 3
    mask = mask.astype(int).diff()

    timestamps_start = pd.to_datetime(df['timestamps'][mask == 1]).tolist()
    timestamps_end = pd.to_datetime(df['timestamps'][mask == -1]).tolist()

    # total duration ready for operating

    total_duration_ready_operating = sum((pd.to_datetime(timestamps_end) - pd.to_datetime(timestamps_start)).total_seconds())
    percentage_ready_operating = 100 * (total_duration_ready_operating / total_duration)
    percentage_unknow = 100 * ((total_duration_at_laparo + total_time_state3 + total_duration_ready_operating) / total_duration)
    # plot

    df['Device_State'] = (df['Device_State'] == 3).astype('int')
    df['Motion_State'] = (df['Motion_State'] == 3).astype('int').apply(lambda x: x*0.9)
    df['timestamps'] = pd.to_datetime(df['timestamps'])
    df['Main_Control_Current_Sub_State'] = ((df['Main_Control_Current_Sub_State'] == 1365).astype('int')).apply(lambda  x: x*(1.1))

    name_laparo = f"Laparo state : {percentage_at_laparo:.2f} %"
    name_motion_state = f"Motion state : {percentage_state3:.2f} %"
    name_ready_operating = f"Ready operating state : {percentage_ready_operating:.2f} %"
    name_unknown = f"Unknown state : {percentage_unknow:.2f} %"
    title = 'Timeline of Laparo state, Motion state and Ready operating state <br><sup>' + get_title_graph(arg) + '</sup>'

    trace_fig = go.Figure()

    trace_fig.add_trace(go.Scatter(
        x=df['timestamps'],
        y=df['Main_Control_Current_Sub_State'],
        mode="markers",
        name=name_laparo,
        marker=dict(
            color="red",
            size=4
        ),
        showlegend=True
    ))

    trace_fig.add_trace(go.Scatter(
        x=df['timestamps'],
        y=df['Device_State'],
        hovertext=df['Device_State'],
        mode="markers",
        name=name_ready_operating,
        marker=dict(
            color="green",
            size=4
        ),
        showlegend=True
    ))


    trace_fig.add_trace(go.Scatter(
        x=df['timestamps'],
        y=df['Motion_State'],
        hovertext=df['Motion_State'],
        mode="markers",
        name=name_motion_state,
        marker=dict(
            color="blue",
            size=4
        ),
        showlegend=True
    ))

    trace_fig.add_trace(go.Scatter(
        x=df['timestamps'],
        y=np.ones(len(df)) * -1,
        mode="markers",
        name=name_unknown,
        marker=dict(
            color="white",
            size=0

        ),
        showlegend=True
    ))

    trace_fig.update_layout(
        title=title,
        autosize=False,
        xaxis_title="Time [h:m]",
        yaxis_range= [0.75, 1.25],
        width=1000,
        height=400
    )


    return trace_fig







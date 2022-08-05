# TODO: implement whatever seems good for visualization


def show_video() -> None:
    pass


#   mp4list = glob.glob('video/*.mp4')
#   if len(mp4list) > 0:
#     mp4 = mp4list[0]
#     video = io.open(mp4, 'r+b').read()
#     encoded = base64.b64encode(video)
#     ipythondisplay.display(HTML(data='''<video alt="test" autoplay
#                 loop controls style="height: 400px;">
#                 <source src="data:video/mp4;base64,{0}" type="video/mp4" />
#              </video>'''.format(encoded.decode('ascii'))))
#   else:
#     print("Could not find video")


def plot_reward(r: int) -> None:
    print(r)
    pass
    # plt.figure(2)
    # plt.clf()
    # plt.title('Result')
    # plt.xlabel('Episode')
    # plt.ylabel('Reward')
    # plt.plot(r)

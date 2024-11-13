from framework.live_data.live_data import LiveData

def onValueChanged(v: int):
    print(f"new data {v}")

if __name__ == '__main__':
    value = LiveData([2992])
    value.changed.observe(onValueChanged)

    value.value = 10
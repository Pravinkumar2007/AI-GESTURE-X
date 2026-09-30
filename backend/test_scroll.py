from scroll import ScrollControl

scroll = ScrollControl()

print("SCROLL + SWIPE MODULE READY")

print(scroll.update_scroll(0.50, 0.50))

print(scroll.update_scroll(0.50, 0.40))

scroll.reset()

print(scroll.update_swipe(0.50, 0.50))

print(scroll.update_swipe(0.80, 0.50))

print("TEST COMPLETED")
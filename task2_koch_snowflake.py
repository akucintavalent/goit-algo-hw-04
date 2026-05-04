import turtle as t


def koch(pen: t.Turtle, length: float, order: int) -> None:
    if order > 0:
        for angle in (60, -120, 60, 0):
            koch(pen, length / 3, order - 1)
            pen.left(angle)
    else:
        pen.forward(length)


def main() -> None:
    size = 400
    try:
        order = int(
            input(
                "Enter the order of the snowflake (non-negative integer, up to 5 is recommended): "
            )
        )
    except ValueError:
        print("Order must be a non-negative integer.")
        return
    if order < 0:
        print("Order must be a non-negative integer.")
        return

    screen = t.Screen()
    screen.bgcolor("black")

    pen = t.Turtle(visible=False)
    pen.color("sky blue", "white")

    # Ensure snowflake is centred
    pen.penup()
    pen.backward(size / 1.732)
    pen.left(30)
    pen.pendown()

    screen.tracer(100)

    pen.begin_fill()

    for _ in range(3):
        koch(pen, size, order)
        pen.right(120)

    pen.end_fill()

    # Draw the last parts
    screen.update()

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

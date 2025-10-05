from manim import *


class LegacyParserScene(Scene):
    """Animation explaining how the current (legacy) parser parses."""

    def construct(self):
        tokens_list = ["2", "^", "3", "*", "4"]

        text = Code(code_string="2 ^ 3 * 4", add_line_numbers=False).to_edge(UP)

        tokens = VGroup(
            [Code(code_string=token, add_line_numbers=False) for token in tokens_list]
        ).arrange(RIGHT, buff=0.5)

        self.play(Write(text))
        self.wait(1)
        self.play(Transform(text, tokens.to_edge(UP)))

        parse_method = Code(code_string="parse()", add_line_numbers=False)
        parse_binary_method = Code(
            code_string="parseBinaryExpression()", add_line_numbers=False
        )
        parse_primary_method = Code(
            code_string="parsePrimaryExpression()", add_line_numbers=False
        )
        methods = (
            VGroup([parse_primary_method, parse_binary_method, parse_method])
            .arrange(UP)
            .to_edge(LEFT)
        )
        method_pointer = Triangle(color=BLUE).scale(0.14)
        method_pointer.rotate(PI / 2)  # point it to the left
        token_pointer = Triangle(color=BLUE).scale(0.14)  # already points upwards
        self.play(Write(methods))

        # so, the parse() method is called by the compiler which is our entrypoint
        self.play(Indicate(methods[2], color=BLUE))
        method_pointer.next_to(methods[2], RIGHT, buff=0.2)
        self.play(Write(method_pointer))

        # look at the first token
        self.play(Indicate(tokens[0], color=GREEN))
        token_pointer.next_to(tokens[0], DOWN, buff=0.2)
        self.play(Write(token_pointer))

        # parse doesn't match any keywords, so it defaults to parseBinaryExpression()
        self.play(Indicate(methods[1], color=BLUE))
        method_pointer.next_to(methods[1], RIGHT, buff=0.2)

        # parseBinaryExpression is called with parentPriority of 0
        parent_priority_tracker = Code(
            code_string="parentPriority = 0", add_line_numbers=False
        ).to_corner(DL)
        self.play(Write(parent_priority_tracker))

        # parseBinaryExpression calls parsePrimaryExpression, which simply returns a number token
        self.play(Indicate(methods[0], color=BLUE))
        method_pointer.next_to(methods[0], RIGHT, buff=0.2)
        token_circle = Circle(radius=0.4, color=BLUE).to_edge(RIGHT, buff=0.5)
        token_number = MathTex("2", color=WHITE)
        token_number.move_to(token_circle.get_center())
        self.play(Write(token_circle))
        self.play(Write(token_number))

        # then we enter the while loop in the parseBinaryExpression function
        self.play(Indicate(methods[1], color=BLUE))
        method_pointer.next_to(methods[1], RIGHT, buff=0.2)

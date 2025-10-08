from manim import *


class LegacyParserScene(Scene):
    """Animation explaining how the current (legacy) parser parses."""

    def construct(self):
        # start with the raw code here
        text = Code(code_string="2 ^ 3 * 4", add_line_numbers=False).to_edge(UP)

        # lex the raw string
        tokens_list = ["2", "^", "3", "*", "4"]
        tokens = VGroup(
            [Code(code_string=token, add_line_numbers=False) for token in tokens_list]
        ).arrange(RIGHT, buff=0.5)

        self.play(Write(text))
        self.wait(1)
        self.play(Transform(text, tokens.to_edge(UP)))

        # these are our methods
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

        # parseBinaryExpression calls parsePrimaryExpression
        self.play(Indicate(methods[0], color=BLUE))
        method_pointer.next_to(methods[0], RIGHT, buff=0.2)
        two_token_circle = Circle(radius=0.4, color=BLUE).to_edge(RIGHT, buff=3)
        token_number = MathTex("2", color=WHITE)
        token_number.move_to(two_token_circle.get_center())
        self.play(Write(two_token_circle))
        self.play(Write(token_number))

        # it returns a number token and advances to the next token
        token_pointer.next_to(tokens[1], DOWN, buff=0.2)

        # then we enter the while loop in the parseBinaryExpression function
        self.play(Indicate(methods[1], color=BLUE))
        method_pointer.next_to(methods[1], RIGHT, buff=0.2)

        # current token is ^ (caret), in the while loop we get the operator priority for this which is 3
        token_priority = Code(
            code_string="priority = 3", add_line_numbers=False
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # is priority === 0 or < parentPriority? both are false, so continue by consuming the caret token
        caret_token_circle = Circle(radius=0.4, color=BLUE).to_edge(UR, buff=2)
        token_number = MathTex("\mathbin{\char`\^}", color=WHITE)
        token_number.move_to(caret_token_circle.get_center())
        self.play(Write(caret_token_circle))
        self.play(Write(token_number))
        token_pointer.next_to(tokens[2], DOWN, buff=0.2)

        # now, recurse by calling parseBinaryExpression with parentPriority = 3
        self.play(Indicate(methods[1], color=BLUE))
        token_priority.remove()
        new_priority = Code(
            code_string="parentPriority = 3", add_line_numbers=False
        ).to_corner(DL)
        self.play(ReplacementTransform(parent_priority_tracker, new_priority))
        parent_priority_tracker = new_priority

        # parseBinaryExpression calls parsePrimaryExpression again
        self.play(Indicate(methods[0], color=BLUE))
        method_pointer.next_to(methods[0], RIGHT, buff=0.2)
        three_token_circle = Circle(radius=0.4, color=BLUE).to_edge(RIGHT, buff=1)
        token_number = MathTex("3", color=WHITE)
        token_number.move_to(three_token_circle.get_center())
        self.play(Write(three_token_circle))
        self.play(Write(token_number))

        # it returns a number token and advances to the next token
        token_pointer.next_to(tokens[3], DOWN, buff=0.2)

        # enter the while loop, inside the recursive call
        self.play(Indicate(methods[1], color=BLUE))
        method_pointer.next_to(methods[1], RIGHT, buff=0.2)

        # current token is *, get the priority which is 2
        token_priority = Code(
            code_string="priority = 2", add_line_numbers=False
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # 2 is less than or equal to the parentPriority, 3, so break and return the number token
        # we are now back in the original call. finally for this iteration, we create a new
        # BinaryExpression and set it to our LHS.
        self.play(Indicate(methods[1], color=BLUE))
        # caret_token_circle.add_line_to(two_token_circle)
        # caret_token_circle.add_line_to(three_token_circle)

        # now we're back in the while loop, with the current token being *
        # get the priority of it
        token_priority = Code(
            code_string="priority = 2", add_line_numbers=False
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # check priority is

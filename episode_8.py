from manim import *

JS_PURPLE = ManimColor("#552856")


class LegacyParserScene(Scene):
    """
    Animation explaining how the current (legacy) parser parses.

    Use BLUE for standard function calls and RED for recursive calls
    """

    def construct(self):
        # start with the raw code here
        raw_code_str = Code(code_string="2 ^ 3 * 4", add_line_numbers=False).to_edge(UP)
        raw_code_str_copy = raw_code_str.copy()

        # lex the raw string
        tokens_list = ["2", "^", "3", "*", "4"]
        tokens = VGroup(
            [
                Code(
                    code_string=token,
                    add_line_numbers=False,
                    language="javascript",
                )
                for token in tokens_list
            ]
        ).arrange(RIGHT, buff=0.5)

        self.play(Write(raw_code_str))
        self.wait(1)
        self.play(Transform(raw_code_str, tokens.to_edge(UP)))
        parse_method = Code(
            code_string="parse()",
            add_line_numbers=False,
            language="javascript",
        )
        parse_binary_method = Code(
            code_string="parseBinaryExpression()",
            add_line_numbers=False,
            language="javascript",
        )
        parse_primary_method = Code(
            code_string="parsePrimaryExpression()",
            add_line_numbers=False,
            language="javascript",
        )
        methods = (
            VGroup([parse_primary_method, parse_binary_method, parse_method])
            .arrange(UP, aligned_edge=LEFT)
            .to_edge(LEFT, buff=1.5)
        )
        self.play(Write(methods))

        normal_text = Text(
            text="BLUE: standard call",
            t2c={"BLUE:": BLUE, "standard call": WHITE},
            disable_ligatures=True,
            color=RED,
            font_size=25,
        )
        recursion_text = Text(
            text="RED: recursive call",
            t2c={"RED:": RED, "recursive call": WHITE},
            disable_ligatures=True,
            color=RED,
            font_size=25,
        )
        self.play(
            Write(
                VGroup(normal_text, recursion_text)
                .arrange(DOWN, aligned_edge=LEFT)
                .to_edge(UL)
            )
        )

        # so, the parse() method is called by the compiler which is our entrypoint
        self.play(Indicate(methods[2], color=BLUE))
        method_pointer = (
            Triangle(color=BLUE)
            .scale(0.14)
            .rotate(PI / 2)
            .next_to(methods[2], buff=0.2)
        )
        self.play(Create(method_pointer))

        # look at the first token
        token_pointer = (
            Triangle(color=WHITE).scale(0.14).next_to(tokens[0], DOWN, buff=0.2)
        )
        self.play(Create(token_pointer))

        # parse doesn't match any keywords, so it defaults to parseBinaryExpression()
        self.play(Indicate(methods[1], color=BLUE))
        parse_to_binary_arrow = DashedVMobject(
            CurvedArrow(
                methods[2].get_left() + (LEFT * 0.1),
                methods[1].get_left() + (LEFT * 0.1) + (UP * 0.2),
                tip_length=0.2,
                color=BLUE,
            ),
            num_dashes=5,
        ).set_stroke(width=2, color=BLUE)
        self.play(Create(parse_to_binary_arrow))
        self.play(method_pointer.animate.next_to(methods[1], RIGHT, buff=0.2))

        # parseBinaryExpression is called with parentPriority of 0
        parent_priority_tracker = Code(
            code_string="parentPriority = 0",
            add_line_numbers=False,
            background_config={"fill_color": BLUE},
        ).to_corner(DL)
        self.play(Write(parent_priority_tracker))

        # parseBinaryExpression calls parsePrimaryExpression, which returns a number token and we advance to next token
        self.play(Indicate(methods[0], color=BLUE))
        binary_to_primary_arrow = DashedVMobject(
            CurvedArrow(
                methods[1].get_left() + (LEFT * 0.1),
                methods[0].get_left() + (LEFT * 0.1),
                tip_length=0.2,
                color=BLUE,
            ),
            num_dashes=5,
        ).set_stroke(width=2, color=BLUE)
        self.play(Create(binary_to_primary_arrow))
        self.play(method_pointer.animate.next_to(methods[0], RIGHT, buff=0.2))
        two_token_circle = Circle(radius=0.4, color=JS_PURPLE).to_edge(RIGHT, buff=3)
        token_number = MathTex("2", color=WHITE)
        token_number.move_to(two_token_circle.get_center())
        two_token = VGroup(token_number, two_token_circle)
        self.play(Create(two_token))
        self.play(token_pointer.animate.next_to(tokens[1], DOWN, buff=0.2))

        # then we enter the while loop in the parseBinaryExpression function
        self.remove(binary_to_primary_arrow)
        self.play(method_pointer.animate.next_to(methods[1], RIGHT, buff=0.2))

        # current token is ^ (caret), in the while loop we get the operator priority for this which is 3
        token_priority = Code(
            code_string="priority = 3",
            add_line_numbers=False,
            background_config={"fill_color": BLUE},
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # is priority === 0 or < parentPriority? both are false, so continue by consuming the caret token
        caret_token_circle = Circle(radius=0.4, color=BLUE).to_edge(UR, buff=2)
        token_number = MathTex("\mathbin{\char`\^}", color=WHITE)
        token_number.move_to(caret_token_circle.get_center())
        caret_token = VGroup(caret_token_circle, token_number)
        self.play(Create(caret_token))
        self.play(token_pointer.animate.next_to(tokens[2], DOWN, buff=0.2))

        # now, recurse by calling parseBinaryExpression with parentPriority = 3
        self.play(Indicate(methods[1], color=RED))

        # NOTE: here I create custom arrow that loops back to itself since Manim doesn't provide this
        binary_to_binary_curve = DashedVMobject(
            CubicBezier(
                start_anchor=methods[1].get_left() + (LEFT * 0.1),
                end_anchor=methods[1].get_left() + (LEFT * 0.1),
                start_handle=methods[1].get_left() + (LEFT * 1.5) + UP,
                end_handle=methods[1].get_left() + (LEFT * 1.5) + DOWN,
            ),
            num_dashes=9,
        ).set_stroke(width=2, color=RED)
        arrow_head = (
            ArrowTriangleFilledTip(fill_color=RED)
            .scale(0.75)
            .rotate(-3 * PI / 4)  # absolute pain to find this value
            .next_to(binary_to_binary_curve, buff=-0.2)
        )
        binary_to_binary_arrow = VGroup(binary_to_binary_curve, arrow_head)
        recursion_pointer = (
            Triangle(color=RED).scale(0.14).rotate(PI / 2).next_to(methods[1], buff=0.6)
        )
        self.play(Create(binary_to_binary_arrow))
        self.play(Create(recursion_pointer))
        self.remove(token_priority)
        new_priority = Code(
            code_string="parentPriority = 3",
            add_line_numbers=False,
            background_config={"fill_color": RED},
        ).to_corner(DL)
        self.play(ReplacementTransform(parent_priority_tracker, new_priority))
        parent_priority_tracker = new_priority

        # parseBinaryExpression calls parsePrimaryExpression again
        self.play(Indicate(methods[0], color=BLUE))
        binary_to_primary_arrow = DashedVMobject(
            CurvedArrow(
                methods[1].get_left() + (LEFT * 0.1),
                methods[0].get_left() + (LEFT * 0.1),
                tip_length=0.2,
                color=RED,
            ),
            num_dashes=5,
        ).set_stroke(width=2, color=RED)
        self.play(Create(binary_to_primary_arrow))
        self.play(recursion_pointer.animate.next_to(methods[0], RIGHT, buff=0.6))
        three_token_circle = Circle(radius=0.4, color=JS_PURPLE).to_edge(RIGHT, buff=1)
        token_number = MathTex("3", color=WHITE)
        token_number.move_to(three_token_circle.get_center())
        three_token = VGroup(token_number, three_token_circle)
        self.play(Create(three_token))

        # it returns a number token and advances to the next token
        self.play(token_pointer.animate.next_to(tokens[3], DOWN, buff=0.2))

        # enter the while loop, inside the recursive call
        self.remove(binary_to_primary_arrow)
        self.play(recursion_pointer.animate.next_to(methods[1], RIGHT, buff=0.6))

        # current token is *, get the priority which is 2
        token_priority = Code(
            code_string="priority = 2",
            add_line_numbers=False,
            background_config={"fill_color": RED},
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # 2 is less than or equal to the parentPriority, 3, so break and return the number token
        # we are now back in the original call. finally for this iteration, we create a new
        # BinaryExpression and set it to our LHS.
        self.remove(recursion_pointer, token_priority, binary_to_binary_arrow)
        new_priority = Code(
            code_string="parentPriority = 0",
            add_line_numbers=False,
            background_config={"fill_color": BLUE},
        ).to_corner(DL)
        self.play(ReplacementTransform(parent_priority_tracker, new_priority))
        parent_priority_tracker = new_priority

        caret_to_two = Line(start=caret_token.get_bottom(), end=two_token.get_top())
        caret_to_three = Line(start=caret_token.get_bottom(), end=three_token.get_top())
        self.play(Create(caret_to_two))
        self.play(Create(caret_to_three))
        lhs = VGroup(two_token, three_token, caret_token, caret_to_three, caret_to_two)
        self.play(lhs.animate.shift(LEFT * 1.65 + DOWN * 1.65))

        # now we're back in the while loop, with the current token being *
        # get the priority of it
        token_priority = Code(
            code_string="priority = 2",
            add_line_numbers=False,
            background_config={"fill_color": BLUE},
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # check priority is equal to zero or less than or equal to parent priority
        # both are false so continue, consume the * token which will be our operator
        star_token_circle = Circle(radius=0.4, color=BLUE).to_edge(UR, buff=2.3)
        token_number = MathTex("*", color=WHITE)
        token_number.move_to(star_token_circle.get_center())
        star_token = VGroup(star_token_circle, token_number)
        self.play(Write(star_token))
        self.play(token_pointer.animate.next_to(tokens[4], direction=DOWN, buff=0.2))

        # finally, we recurse parseBinaryExpression() with the current priority 2
        self.play(Create(binary_to_binary_arrow))
        self.play(Create(recursion_pointer))
        self.remove(token_priority)
        new_priority = Code(
            code_string="parentPriority = 2",
            add_line_numbers=False,
            background_config={"fill_color": RED},
        ).to_corner(DL)
        self.play(ReplacementTransform(parent_priority_tracker, new_priority))

        # this calls parsePrimaryExpression(), which consumes the 4 token and returns it
        self.play(Indicate(methods[0], color=BLUE))
        binary_to_primary_arrow = DashedVMobject(
            CurvedArrow(
                methods[1].get_left() + (LEFT * 0.1),
                methods[0].get_left() + (LEFT * 0.1),
                tip_length=0.2,
                color=RED,
            ),
            num_dashes=5,
        ).set_stroke(width=2, color=RED)
        self.play(Create(binary_to_primary_arrow))
        self.play(recursion_pointer.animate.next_to(methods[0], RIGHT, buff=0.6))
        four_token_circle = Circle(radius=0.4, color=JS_PURPLE).next_to(
            caret_token_circle.get_center() + (RIGHT * 2)
        )
        token_number = MathTex("4", color=WHITE)
        token_number.move_to(four_token_circle.get_center())
        four_token = VGroup(token_number, four_token_circle)
        self.play(Create(four_token))

        # then we enter the while loop of parseBinary
        self.remove(binary_to_primary_arrow)
        self.play(recursion_pointer.animate.next_to(methods[1], RIGHT, buff=0.6))

        # priority defaults to zero so we break from the loop immediately
        # return the 4 token from the recursive call, which becomes our new right token
        token_priority = Code(
            code_string="priority = 0",
            add_line_numbers=False,
            background_config={"fill_color": RED},
        ).next_to(parent_priority_tracker, RIGHT, buff=0.2)
        self.play(Write(token_priority))

        # and we return a new binary expression class looking like the tree on the animation
        self.remove(
            recursion_pointer,
            binary_to_binary_arrow,
            token_priority,
            new_priority,
        )
        star_to_caret = Line(start=star_token.get_bottom(), end=caret_token.get_top())
        star_to_four = Line(start=star_token.get_bottom(), end=four_token.get_top())
        self.play(Create(star_to_caret))
        self.play(Create(star_to_four))

        self.remove(parse_to_binary_arrow)
        self.play(method_pointer.animate.next_to(methods[2], RIGHT, buff=0.2))

        final_tree = VGroup(lhs, star_to_caret, star_to_four, star_token, four_token)

        for obj in self.mobjects:
            if obj != final_tree:
                self.remove(obj)

        self.play(final_tree.animate.shift(LEFT * 4.4))
        self.play(Write(raw_code_str_copy))

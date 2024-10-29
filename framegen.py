import math
from pathlib import Path
from string import Template

HTML_TEMPLATE_PATH = Path("templates/base.template.html")
CLOCK_SVG_TEMPLATE_PATH = Path("templates/clock.template.svg")

TITLE = "12 hours all at once / Even a stopped clock is right twice a day"

def main():
    svg_template = load_template(path=CLOCK_SVG_TEMPLATE_PATH)
    html_template = load_template(path=HTML_TEMPLATE_PATH)

    content = generate_all_clock_frames(svg_template=svg_template, size=400, clock_radius=150)
    with open("pages/clock-frames.html", "w+") as fp:
        fp.write(html_template.safe_substitute(title=TITLE, content=content))
    

def generate_all_clock_frames(svg_template: Template, size: float, clock_radius: float) -> str:
    center = size / 2
    ticks = generate_ticks(center=center, inner_radius=clock_radius * 0.8, outer_radius=clock_radius * 0.95)
    return "".join([
        generate_clock_frame(
            svg_template=svg_template, 
            clock_radius=clock_radius,
            size=size,
            center=center,
            hour=hour, 
            minute=minute,
            ticks=ticks,
        )
        for hour in range(12)
        for minute in range(60)
    ])


def calculate_hand_angles(hour, minute):
    hour_angle = 180 - ((hour % 12) * 30 + (minute / 60) * 30) # Hour hand moves 0.5 degrees per minute
    minute_angle = minute * 6  # Minute hand moves 6 degrees per minute
    return hour_angle, minute_angle


def generate_clock_frame(
    svg_template: Template, 
    center: float, 
    size: float, 
    hour: float, 
    minute: float, 
    ticks: str, 
    clock_radius: float
) -> str:
    minute_hand_outer_radius = clock_radius * 0.9
    hour_hand_outer_radius = clock_radius * 0.6

    hour_angle, minute_angle = calculate_hand_angles(hour=hour, minute=minute)
    template_values = dict(
        hour=f"{hour:02}",
        minute=f"{minute:02}",
        hour_x2=center + hour_hand_outer_radius * math.sin(math.radians(hour_angle)),
        hour_y2=center + hour_hand_outer_radius * math.cos(math.radians(hour_angle)),
        minute_x2=center + minute_hand_outer_radius * math.sin(math.radians(minute_angle)),
        minute_y2=center - minute_hand_outer_radius * math.cos(math.radians(minute_angle)),
        ticks=ticks,
        center=center,
        clock_radius=clock_radius,
        size=size,
    )
    return svg_template.safe_substitute(template_values)

def generate_ticks(center: float, inner_radius: float, outer_radius: float) -> str:
    ticks = []
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = center + inner_radius * math.cos(angle)
        y1 = center - inner_radius * math.sin(angle)
        x2 = center + outer_radius * math.cos(angle)
        y2 = center - outer_radius * math.sin(angle)
        ticks.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#444" stroke-width="4"/>')
    
    return "".join(ticks)

def load_template(path: Path) -> Template:
    with open(path) as fp:
        return Template(fp.read())


if __name__ == "__main__":
    main()
#!/usr/bin/env python

from pathlib import Path
import os
import typing
import subprocess
import itertools

WALLPAPER_HOME = Path(os.environ["HOME"]) / ".wallpapers"
PathGroup = list[Path]


class Wallpapers:
    def __init__(self, path: Path):
        self.path_var: Path = path
        self.imgs: PathGroup = self.get_imgs()
        self.current_wall: str = self.get_current_wall()
        self.index_num: int = self.get_index()

    def get_imgs(self) -> PathGroup:
        imgs: PathGroup = []
        for child in self.path_var.iterdir():
            if child.name.split(".")[1] in ["gif", "jpg", "png"]:
                imgs.append(child)
        return imgs

    def get_current_wall(self) -> str:
        with subprocess.Popen("swww query", shell=True, stdout=subprocess.PIPE) as proc:
            self.value: str = proc.stdout.read().decode("utf-8").rstrip()
            self.file: str = self.value.split("hm_img/")[1]
        return self.file

    def get_index(self) -> int:
        self.imgs_as_strs = [str(element) for element in self.imgs]
        self.current_wall_path_str = str(self.path_var) + "/" + self.current_wall
        return self.imgs_as_strs.index(self.current_wall_path_str)

    def new_wallpaper(
        self,
        wallpaper_to_show,
        transition_fps: int,
        transition_type: str,
        transition_pos1: float,
        transition_pos2: float,
        transition_duration: int,
    ):
        command = f"swww img {wallpaper_to_show} --transition-fps {transition_fps} --transition-type {transition_type} --transition-pos {transition_pos1},{transition_pos2} --transition-duration {transition_duration}"
        print(command)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as proc:
            print(proc.stdout.read().decode("utf-8").rstrip())


if __name__ == "__main__":
    wallpapers = Wallpapers(WALLPAPER_HOME)
    next_wallpaper = str(wallpapers.imgs[wallpapers.index_num])
    wallpapers.new_wallpaper(next_wallpaper, 244, "outer", 0.854, 0.977, 1)

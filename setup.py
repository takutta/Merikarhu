from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import shutil
import subprocess
import zipfile


class CustomInstall(install):
    def run(self):
        # Luo kohdekansio
        dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
        install_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "dist", "merikarhu"
        )
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # Poista kohdekansion sisältö
        for root, dirs, files in os.walk(install_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)

        # Hae asennetut paketit virtuaaliympäristöstä
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        packages = result.stdout.splitlines()

        # Kirjoita paketit requirements-tiedostoon
        requirements_file_path = os.path.join(install_dir, "requirements.txt")
        with open(requirements_file_path, "w") as requirements_file:
            requirements_file.writelines(packages)

        # Kopioi tiedostot kohdekansioon
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_list = [
            "merikarhu.py",
            "titania.py",
            "tarvetaulukko.py",
            "requirements.txt",
            "peukku.png",
            "merikarhu.ico",
            "merikarhu_helper.py",
            "luokat.py",
            "hylje.png",
            "excel.py",
        ]
        templates = ["tarvetaulukko.jinja"]
        build = [
            "build\\js\\bootstrap.bundle.min.js",
            "build\\js\\jquery-3.6.0.min.js",
            "build\\js\\loader.js",
            "build\\js\\plotly.js",
            "build\\js\\resize.js",
            "build\\js\\scrollspy.js",
            "build\\js\\mini.js",
            "build\\js\\tabs.js",
            "build\\css\\minty.min.css",
            "build\\css\\style.css",
        ]
        other = ["other\\asenna.bat"]

        for file in file_list:
            shutil.copy2(os.path.join(base_dir, file), os.path.join(install_dir, file))

        # Luo input-kansio
        input_dir = os.path.join(install_dir, "merikarhu", "input")
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)

        # Luo output-kansio
        output_dir = os.path.join(install_dir, "merikarhu", "output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        templates_dir = os.path.join(install_dir, "templates")
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)

        for template in templates:
            shutil.copy2(
                os.path.join(base_dir, "templates", template),
                os.path.join(templates_dir, template),
            )

        build_dir = os.path.join(install_dir, "build")
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        for file in build:
            file_path = os.path.join(base_dir, file)
            target_path = os.path.join(install_dir, file.replace("build/", ""))
            target_dir = os.path.dirname(target_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            shutil.copy2(file_path, target_path)

        for file in other:
            shutil.copy2(
                os.path.join(base_dir, file),
                os.path.join(dist_dir, os.path.basename(file)),
            )
        # Paketoi tiedostot ZIP-muotoon
        zip_file_path = os.path.join(dist_dir, "merikarhu.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zip_file:
            for root, dirs, files in os.walk(dist_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.endswith(".zip"):
                        continue  # Ohita zip-tiedostot
                    zip_file.write(file_path, os.path.relpath(file_path, dist_dir))

        dist_zip_file_path = os.path.join(dist_dir, "merikarhu.zip")
        shutil.move(zip_file_path, dist_zip_file_path)


setup(
    name="Merikarhu",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "plotly",
    ],
    cmdclass={
        "install": CustomInstall,
    },
)

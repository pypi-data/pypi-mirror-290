import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HMautogroup", # 모듈 이름
    version="0.1.0", # 버전
    author="KDPark", # 제작자
    author_email="k602511@gmail.com", # contact
    description="auto-cleaning-grouping-process", # 모듈 설명
    long_description=open('README.md').read(), # README.md에 보통 모듈 설명을 해놓는다.
    long_description_content_type="text/markdown",
    url="https://github.com/kdpark0284/HM_titledescription_filtering",
    project_url={
        "Bug Tracker": "https://github.com/kdpark0284/HM_titledescription_filtering/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[ # 필수 라이브러리들을 포함하는 부분인 것 같음, 다른 방식으로 넣어줄 수 있는지는 알 수 없음
    "openpyxl==3.1.5", 
    "numpy==1.26.4", 
    "pandas==2.1.4", 
    "regex==2024.5.15", 
    "google-colab==1.0.0", 
    "konlpy==0.6.0", 
    "setuptools==71.0.4",
    "mecab-python==1.0.0",
    "mecab-python3==1.0.9",
    "rapidfuzz==3.9.6",
    "jamo==0.4.1"
    ],
    package_dir={"": "lib"},
    package_data={'': ['LICENSE.txt', 'requirements.txt']}, # 원하는 파일 포함, 제대로 작동되지 않았음
    include_package_data=True,
    packages = setuptools.find_packages(), # 모듈을 자동으로 찾아줌
    python_requires=">=3.10.12", # 파이썬 최소 요구 버전
)
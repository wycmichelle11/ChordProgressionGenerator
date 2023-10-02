# Chord Progression Generator
Extract the chord progression of a song from a Youtube song link
install virtual environment
```python -m venv env```<br>
activate virtual environment
```.\env\Scripts\activate```<br>
install pytube
```pip install pytube```<br>
install librosa
```pip install librosa```<br>

To run:
```python flaskApp.py```<br>
<img width="960" alt="image" src="https://github.com/wycmichelle11/ChordProgressionGenerator/assets/79016649/fcc26db8-a094-402a-b88f-8e46a0944112"> <br>
Then enter Youtube Link of the song you want to know the chord progression of. Need to consider copyright legal issues. The link in the image is a non-copyrighted song.<br>
<img width="960" alt="image" src="https://github.com/wycmichelle11/ChordProgressionGenerator/assets/79016649/e27d450e-dae2-47d5-87ea-59b22d88a639"><br>
Select submit then just wait.<br>
In a few moments, the chord progression will be displayed.<br>
<img width="960" alt="image" src="https://github.com/wycmichelle11/ChordProgressionGenerator/assets/79016649/1f576dea-14e5-47d0-87ba-ba60a26d3c9a"><br><br>
There are a lot of chord for the whole song. As an iterative process, it would be useful to find patterns in the chord progression and narrow it down to the progression that is repeating. 
Additionally, as time progresses, it would be useful to use a machine learning process to correct the extraction to make sure it is accurate.

import React, {useState} from 'react';
import './App.css';
import wordsData from './words_data.json'
import _ from 'lodash'

function getPath() {
  const data = wordsData["8"];
  while (true) {
    const seen = {};
    const path = [];
    let node = _.sample(_.keys(data));
    while (true) {
      seen[node] = true;
      const [words, neighbors] = data[node];
      path.push(_.sample(words));
      const options = neighbors.filter(x => !seen[x]);
      if (!options.length) {
        if (path.length > 200) {
          return path;
        }
        break;
      }
      node = _.sample(options);
    }
  }
}

const PATH = getPath();

function App() {
  const num_actual_options = 7;
  const [message, setMessage] = useState("");
  const [options, setOptions] = useState(
    _.shuffle([...PATH.slice(0, num_actual_options), "", "", ""])
  );
  const [letters, setLetters] = useState(
    _.shuffle([...PATH[0]])
  );
  const [pathIndex, setPathIndex] = useState(0);

  return (
    <div className="App">
      <div className="options-list">
        {options.map((option, optionIndex) =>
          <div
            key={optionIndex}
            className={`letters-row ${option ? "actual-option" : "option-placeholder"}`}
            onClick={() => {
              if (!option) return;

              console.log(PATH[pathIndex], option)

              if (PATH[pathIndex] === option) {
                const emptyIndices = options
                  .map(((value, index) => [value, index]))
                  .filter(([value]) => !value)
                  .map(([, index]) => index);

                const newIndex = _.sample(emptyIndices);
                options[newIndex] = PATH[pathIndex + num_actual_options]
                options[optionIndex] = "";
                setOptions(options);
                setLetters(_.shuffle([...PATH[pathIndex + 1]]));
                setPathIndex(pathIndex + 1);
                setMessage("Correct!");
              } else {
                setMessage("Wrong!");
              }

            }}
          >
            {option}
          </div>
        )}
      </div>
      <div className="right-half">
        <div className="status-message">{message}</div>
        <div className="scrambled-letters">{blockLetters(letters)}</div>
      </div>

    </div>
  );
}

const blockLetters = (letters) =>
  <div className="letters-row">
    {[...letters].map(letter =>
      <span className="letter-block">
        {letter}
      </span>
    )}
  </div>

export default App;

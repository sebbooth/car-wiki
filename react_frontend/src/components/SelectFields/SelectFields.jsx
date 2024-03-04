import { useEffect, useState, useMemo, useContext } from "react";
import { SearchContext } from "../../contexts/SearchContext";

import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import ListItemText from "@mui/material/ListItemText";
import Select from "@mui/material/Select";
import Checkbox from "@mui/material/Checkbox";
import "./SelectFields.scss";
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const SelectFields = (props) => {
  const { changeSearchFields } = useContext(SearchContext);
  const [selectedFields, setSelectedFields] = useState([]);

  useEffect(() => {
    changeSearchFields(props.category, selectedFields);
  }, [selectedFields]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedFields(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  return (
    <div className="select-fields-container">
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">
          {props.category}
        </InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={selectedFields}
          onChange={handleChange}
          input={<OutlinedInput label={props.category} />}
          renderValue={(selected) => selected.join(", ")}
          MenuProps={MenuProps}
        >
          {props.fields.map((field) => (
            <MenuItem key={field} value={field}>
              <Checkbox checked={selectedFields.indexOf(field) > -1} />
              <ListItemText primary={field} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};

export default SelectFields;

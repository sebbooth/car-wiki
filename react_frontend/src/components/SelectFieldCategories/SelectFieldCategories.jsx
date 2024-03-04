import React from "react";
import { useEffect, useContext, useState, useMemo } from "react";
import "./SelectFieldCategories.scss";
import { db, auth } from "../../config/firebase";
import {
  getDocs,
  collection,
  addDoc,
  deleteDoc,
  updateDoc,
  doc,
  getDoc,
  Timestamp,
} from "firebase/firestore";
import { SearchContext } from "../../contexts/SearchContext";
import { SelectFields } from "../";

import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import ListItemText from "@mui/material/ListItemText";
import Select from "@mui/material/Select";
import Checkbox from "@mui/material/Checkbox";

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

function findCategory(array, category) {
  for (let i = 0; i < array.length; i++) {
    if (array[i].category === category) {
      return array[i];
    }
  }
  return null;
}

const SelectFieldCategories = () => {
  const [allFieldCategories, setAllFieldCategories] = useState([]);

  const [selectedCategories, setSelectedCategories] = useState([]);
  const { changeSearchFields } = useContext(SearchContext);

  useEffect(() => {
    for (const catI in allFieldCategories) {
      const catName = allFieldCategories[catI].category;
      if (!selectedCategories.includes(catName)) {
        changeSearchFields(catName, []);
      }
    }
  }, [selectedCategories]);

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedCategories(
      // On autofill we get a stringified value.
      typeof value === "string" ? value.split(",") : value
    );
  };

  const vehiclesCollectionRef = useMemo(() => {
    return collection(db, "testFieldsByCategory");
  }, []);

  const getAllFields = async () => {
    try {
      const data = await getDocs(vehiclesCollectionRef);
      console.log("getAllFields");
      const filteredData = data.docs.map((doc) => ({
        ...doc.data(),
        id: doc.id,
      }));
      setAllFieldCategories(filteredData);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    getAllFields();
  }, []);

  return (
    <div className="select-categories-container">
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id="demo-multiple-checkbox-label">Category</InputLabel>
        <Select
          labelId="demo-multiple-checkbox-label"
          id="demo-multiple-checkbox"
          multiple
          value={selectedCategories}
          onChange={handleChange}
          input={<OutlinedInput label="Category" />}
          renderValue={(selected) => selected.join(", ")}
          MenuProps={MenuProps}
        >
          {allFieldCategories.map((fieldCategory) => (
            <MenuItem
              key={fieldCategory.category}
              value={fieldCategory.category}
            >
              <Checkbox
                checked={
                  selectedCategories.indexOf(fieldCategory.category) > -1
                }
              />
              <ListItemText primary={fieldCategory.category} />
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <div className="categories-container">
        {selectedCategories.map((fieldCategory) => {
          const categoryObj = findCategory(allFieldCategories, fieldCategory);
          return (
            <SelectFields
              key={categoryObj.category}
              fields={categoryObj.fields}
              category={categoryObj.category}
            />
          );
        })}
      </div>
    </div>
  );
};

export default SelectFieldCategories;

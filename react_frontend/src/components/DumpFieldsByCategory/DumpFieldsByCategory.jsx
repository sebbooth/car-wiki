import React from "react";
import { useMemo } from "react";
import { db, auth } from "../../config/firebase";
import {
  collection,
  addDoc,
  query,
  where,
  getCountFromServer,
} from "firebase/firestore";

import rawData from "../../../../data_mine/selenium/wikipedia/output/vehicles.json";

function createEmptyObjectWithAllFields(collection) {
  const result = [];

  collection.forEach((obj) => {
    addFieldsToResult(obj, result, "General");
  });

  return result;
}

function addFieldsToResult(obj, result, category) {
  for (const key in obj) {
    if (typeof obj[key] === "object" && obj[key] !== null) {
      addFieldsToResult(obj[key], result, key);
    } else if (obj[key] !== "") {
      let fieldCategory = findCategory(result, category);
      if (fieldCategory != null) {
        if (!fieldCategory.fields.includes(key)) fieldCategory.fields.push(key);
      } else {
        fieldCategory = {};
        fieldCategory.category = category;
        fieldCategory.fields = [key];
        result.push(fieldCategory);
      }
    }
  }
}

function findCategory(array, category) {
  for (let i = 0; i < array.length; i++) {
    if (array[i].category === category) {
      return array[i];
    }
  }
  return null;
}

const DumpFields = () => {
  const emptyObjectWithAllFields = createEmptyObjectWithAllFields(rawData);
  //console.log(emptyObjectWithAllFields);
  const fieldsCollectionRef = useMemo(() => {
    return collection(db, "testFieldsByCategory");
  }, []);

  const dumpField = async (fieldCategory) => {
    let exists = -1;

    try {
      const q = query(
        fieldsCollectionRef,
        where("category", "==", fieldCategory.category)
      );
      const snapshot = await getCountFromServer(q);
      exists = snapshot.data().count;
    } catch (err) {
      console.error(err);
    }

    if (exists == 0) {
      try {
        await addDoc(fieldsCollectionRef, {
          ...fieldCategory,
        });
        console.log("add fieldCategory");
      } catch (err) {
        console.error(err);
      }
    }
  };

  const onDumpFields = () => {
    emptyObjectWithAllFields.map((fieldCategory) => {
      dumpField(fieldCategory);
    });
  };

  return (
    <div>
      <button onClick={onDumpFields}>Dump fields by category</button>
    </div>
  );
};

export default DumpFields;

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
      let fieldObj = {};
      fieldObj["field"] = key;
      fieldObj["category"] = category;
      if (!isDuplicate(result, fieldObj)) {
        result.push(fieldObj);
      }
    }
  }
}

function isDuplicate(array, obj) {
  for (let i = 0; i < array.length; i++) {
    if (array[i].field === obj.field && array[i].category === obj.category) {
      return true;
    }
  }
  return false;
}

const DumpFields = () => {
  const emptyObjectWithAllFields = createEmptyObjectWithAllFields(rawData);

  const fieldsCollectionRef = useMemo(() => {
    return collection(db, "testFields");
  }, []);

  const dumpField = async (field) => {
    let exists = -1;

    try {
      const q = query(
        fieldsCollectionRef,
        where("field", "==", field.field),
        where("category", "==", field.category)
      );
      const snapshot = await getCountFromServer(q);
      exists = snapshot.data().count;
    } catch (err) {
      console.error(err);
    }

    if (exists == 0) {
      try {
        await addDoc(fieldsCollectionRef, {
          ...field,
        });
        console.log("add field");
      } catch (err) {
        console.error(err);
      }
    }
  };

  const onDumpFields = () => {
    emptyObjectWithAllFields.map((field) => {
      dumpField(field);
    });
  };

  return (
    <div>
      <button onClick={onDumpFields}>Dump fields</button>
    </div>
  );
};

export default DumpFields;

import { useState } from "react";
import { auth, storage } from "../../config/firebase";
import { ref, uploadBytes } from "firebase/storage";

const FileUpload = () => {
  const [fileUpload, setFileUpload] = useState(null);

  const uploadFile = async () => {
    if (!fileUpload) return;
    try {
      const filesFolderRef = ref(storage, `testFolder/${fileUpload.name}`);
      await uploadBytes(filesFolderRef, fileUpload);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setFileUpload(e.target.files[0])} />
      <button onClick={uploadFile}>Upload Image</button>
    </div>
  );
};

export default FileUpload;

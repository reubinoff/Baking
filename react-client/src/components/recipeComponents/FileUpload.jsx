import { styled } from "@mui/material/styles";
import {
  Box,
  FormHelperText,
  IconButton,
  Stack,
  Typography,
} from "@mui/material";
import { useCallback, useEffect, useRef, useState } from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import {
  useForm,
} from "react-hook-form";
import { PropTypes } from "prop-types";
import png from "../../assets/png.png";
import jpg from "../../assets/jpg.png";
import svg from "../../assets/svg.png";
import defaultImage from "../../assets/default.png";
import jpeg from "../../assets/jpeg.png";

const ImageConfig = {
  png,
  jpg,
  svg,
  "svg+xml": svg,
  default: defaultImage,
  jpeg,
};

const CustomBox = styled(Box)({
  "&.MuiBox-root": {
    backgroundColor: "#fff",
    borderRadius: "2rem",
    boxShadow: "rgba(149, 157, 165, 0.2) 0px 8px 24px",
    padding: "1rem",
  },
  "&.MuiBox-root:hover, &.MuiBox-root.dragover": {
    opacity: 0.6,
  },
});

export default function FileUpload(props) {
  const { name, limit, multiple } = props;

  const { isSubmitting, errors } = useForm();

  const [singleFile, setSingleFile] = useState([]);
  const [fileList, setFileList] = useState([]);
  const wrapperRef = useRef(null);
  const ref = useRef(null);

  const onDragEnter = () => wrapperRef.current?.classList.add("dragover");
  const onDragLeave = () => wrapperRef.current?.classList.remove("dragover");
  //   const onFileDrop = (e) => console.log(e);
  const onFileDrop = useCallback(
    (e) => {
      const target = e.target;
      if (!target.files) return;

      if (limit === 1) {
        const newFile = Object.values(target.files).map((file) => file);
        if (singleFile.length >= 1) return alert("Only a single image allowed");
        setSingleFile(newFile);
        ref.onChange(newFile[0]);
      }

      if (multiple) {
        const newFiles = Object.values(target.files).map((file) => file);
        const exists = newFiles.filter((file) =>
          fileList.find((f) => f.name === file.name)
        );
        if (exists.length > 0) {
          return alert("File already exists");
        }
        if (newFiles) {
          const updatedList = [...fileList, ...newFiles];
          if (updatedList.length > limit || newFiles.length > 3) {
            return alert(`Image must not be more than ${limit}`);
          }
          setFileList(updatedList);
          ref.onChange(updatedList);
        }
      }
    },
    [fileList, limit, multiple, singleFile]
  );

  const fileRemove = (file) => {
    const updatedList = [...fileList];
    updatedList.splice(fileList.indexOf(file), 1);
    setFileList(updatedList);
  };

  const fileSingleRemove = () => {
    setSingleFile([]);
  };

  // ? Calculate Size in KiloByte and MegaByte
  const calcSize = (size) => {
    return size < 1000000
      ? `${Math.floor(size / 1000)} KB`
      : `${Math.floor(size / 1000000)} MB`;
  };

  useEffect(() => {
    if (isSubmitting) {
      setFileList([]);
      setSingleFile([]);
    }
  }, [isSubmitting]);

  return (
    <>
      <CustomBox>
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          sx={{
            position: "relative",
            width: "100%",
            height: "6rem",
            border: "2px dashed #4267b2",
            borderRadius: "20px",
          }}
          ref={wrapperRef}
          onDragEnter={onDragEnter}
          onDragLeave={onDragLeave}
          onDrop={onDragLeave}
        >
          <Stack justifyContent="center" sx={{ p: 1, textAlign: "center" }}>
            <Typography sx={{ color: "#ccc" }}>
              {limit > 1 ? "Browse files to upload" : "Browse file to upload"}
            </Typography>
            <div>
              <CloudUploadIcon />
            </div>
            <Typography variant="body1" component="span">
              <strong>Supported Files</strong>
            </Typography>
            <Typography variant="body2" component="span">
              JPG, JPEG, PNG
            </Typography>
          </Stack>

          <input
            type="file"
            ref={ref}
            name={name}
            onChange={onFileDrop}
            onClick={(e) => (e.target.value = null)}
            multiple={multiple}
            accept="image/jpg, image/png, image/jpeg"
            style={{
              opacity: 0,
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              cursor: "pointer",
            }}
          />
        </Box>
      </CustomBox>

      <FormHelperText
        sx={{ textAlign: "center", my: 1 }}
        error={!!errors?.name}
      >
        {errors?.name ? errors?.name?.message : ""}
      </FormHelperText>

      {/* ?Image Preview ? */}
      {fileList.length > 0 || singleFile.length > 0 ? (
        <Stack spacing={2} sx={{ my: 2 }}>
          {(multiple ? fileList : singleFile).map((item, index) => {
            const imageType = item.type.split("/")[1];
            return (
              <Box
                key={index}
                sx={{
                  position: "relative",
                  backgroundColor: "#f5f8ff",
                  borderRadius: 1.5,
                  p: 0.5,
                }}
              >
                <Box display="flex">
                  <img
                    src={ImageConfig[`${imageType}`] || ImageConfig["default"]}
                    alt="upload"
                    style={{
                      height: "3rem",
                      objectFit: "contain",
                    }}
                  />
                  <Box sx={{ ml: 1 }}>
                    <Typography variant="body2" >{item.name}</Typography>
                    <Typography variant="body2">
                      {calcSize(item.size)}
                    </Typography>
                  </Box>
                </Box>
                <IconButton
                  onClick={() => {
                    if (multiple) {
                      fileRemove(item);
                    } else {
                      fileSingleRemove();
                    }
                  }}
                  sx={{
                    color: "#df2c0e",
                    position: "absolute",
                    right: "1rem",
                    top: "50%",
                    transform: "translateY(-50%)",
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            );
          })}
        </Stack>
      ) : null}
    </>
  );
}

FileUpload.propTypes = {
  name: PropTypes.string.isRequired,
  multiple: PropTypes.bool,
  limit: PropTypes.number.isRequired,
};

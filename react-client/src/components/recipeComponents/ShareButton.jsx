import React from "react";
import Box from "@mui/material/Box";
import SpeedDial from "@mui/material/SpeedDial";
import { styled } from "@mui/material/styles";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import FacebookOutlinedIcon from "@mui/icons-material/FacebookOutlined";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import EmailIcon from "@mui/icons-material/Email";
import ShareRoundedIcon from "@mui/icons-material/ShareRounded";
import { PropTypes } from "prop-types";

function isMobileOrTablet() {
  return /(android|iphone|ipad|mobile)/i.test(navigator.userAgent);
}

function GetRecipeUrl(recipe) {
  const url = `https://app.baking.reubinoff.com/recipe/${recipe.id}`;
  return url;
}


export default function ShareButton(params) {
  const { recipe } = params;
  const StyledSpeedDial = styled(SpeedDial)(({ theme }) => ({
    "&.MuiSpeedDial-directionRight": {
      top: theme.spacing(2),
      left: theme.spacing(2),
    },
  }));

  const shareToWhatsapp = () => {
    const message = `🍞 Check out this recipe *${
      recipe.name
    }* I found on: ${GetRecipeUrl(recipe)}`;
    const tempUrl = "https://" + (isMobileOrTablet() ? "api" : "web");
    const url = `${tempUrl}.whatsapp.com/send?text=${encodeURIComponent(
      message
    )}`;
    window.open(url, "_blank");
  };

  const shareToFacebook = () => {
    const url_to_share = GetRecipeUrl(recipe);
    const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
      url_to_share
    )}&t=${encodeURIComponent(
      `Check out this recipe ${recipe.name} I found on`
    )}`;
    window.open(url, "_blank");
  };

  const shareToEmail = () => {
    const message = `Check out this recipe ${recipe.name} I found on: ${GetRecipeUrl(recipe)}`;
    const url = `mailto:?subject=subject&body=${encodeURIComponent(message)}`;
    window.open(url, "_blank");
  };

  const [actions] = React.useState(
    [
    {
      icon: <FacebookOutlinedIcon onClick={shareToFacebook} />,
      name: "Facebook",
    },
    { icon: <WhatsAppIcon onClick={shareToWhatsapp} />, name: "WhatsApp" },
    { icon: <EmailIcon onClick={shareToEmail} />, name: "Email" },
  ]);

  const actionItems = React.useMemo(() => {
    const items = actions.map((action) => (
      <SpeedDialAction
        key={action.name}
        icon={action.icon}
        tooltipTitle={action.name}
      />
    ));
    return items;
  }, [actions]);


  return (
    <Box sx={{ transform: "translateZ(0px)", flexGrow: 1 }}>
      <StyledSpeedDial
        ariaLabel="SpeedDial playground example"
        icon={<ShareRoundedIcon />}
        direction="right"
        FabProps={{ size: "small" }}
        sx={{
          "& .MuiFab-primary": {
            backgroundColor: "transparent",
            color: "black",
            boxShadow: "none",

            "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.04)" },
          },
        }}
      >
        {actionItems}
      </StyledSpeedDial>
    </Box>
  );
}

ShareButton.propTypes = {
  recipe: PropTypes.object.isRequired,
};

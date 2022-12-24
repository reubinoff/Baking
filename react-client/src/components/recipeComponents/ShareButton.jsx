import Box from "@mui/material/Box";
import SpeedDial from "@mui/material/SpeedDial";
import { styled } from "@mui/material/styles";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import FacebookOutlinedIcon from "@mui/icons-material/FacebookOutlined";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import EmailIcon from "@mui/icons-material/Email";
import ShareRoundedIcon from "@mui/icons-material/ShareRounded";

function isMobileOrTablet() {
  return /(android|iphone|ipad|mobile)/i.test(navigator.userAgent);
}


export default function ShareButton(params) {
  const StyledSpeedDial = styled(SpeedDial)(({ theme }) => ({
    "&.MuiSpeedDial-directionRight": {
      top: theme.spacing(2),
      left: theme.spacing(2),
    },
  }));

  const shareToWhatsapp = () => {
    const message =
      "Check out this recipe on: https://app.baking.reubinoff.com/";
    const tempUrl = "https://" + (isMobileOrTablet() ? "api" : "web"); 
    const url = `${tempUrl}.whatsapp.com/send?text=${encodeURIComponent(
      message
    )}`;
    window.open(url, "_blank");
  };

  const shareToFacebook = () => {
    const message =
      "Check out this recipe on: https://app.baking.reubinoff.com/";
    const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
      message
    )}`;
    window.open(url, "_blank");
  };

  const shareToEmail = () => {
    const message =
      "Check out this recipe on: https://app.baking.reubinoff.com/";
    const url = `mailto:?subject=subject&body=${encodeURIComponent(message)}`;
    window.open(url, "_blank");
  };

  const actions = [
    {
      icon: <FacebookOutlinedIcon onClick={shareToFacebook} />,
      name: "Facebook",
    },
    { icon: <WhatsAppIcon onClick={shareToWhatsapp} />, name: "WhatsApp" },
    { icon: <EmailIcon onClick={shareToEmail} />, name: "Email" },
  ];

  return (
    <Box sx={{ transform: "translateZ(0px)", flexGrow: 1 }}>
      <StyledSpeedDial
        ariaLabel="SpeedDial playground example"
        icon={<ShareRoundedIcon />}
        direction="right"
        FabProps={{ size: "small" }}
      >
        {actions.map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            tooltipTitle={action.name}
          />
        ))}
      </StyledSpeedDial>
    </Box>
  );
}

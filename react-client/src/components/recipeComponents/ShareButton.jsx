import Box from "@mui/material/Box";
import SpeedDial from "@mui/material/SpeedDial";
import { styled } from "@mui/material/styles";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import FacebookOutlinedIcon from "@mui/icons-material/FacebookOutlined";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import EmailIcon from "@mui/icons-material/Email";
import ShareRoundedIcon from "@mui/icons-material/ShareRounded";

export default function ShareButton(params) {
const StyledSpeedDial = styled(SpeedDial)(({ theme }) => ({
  "&.MuiSpeedDial-directionDown, &.MuiSpeedDial-directionRight": {
    top: theme.spacing(2),
    left: theme.spacing(2),
  },
}));

  const actions = [
    { icon: <FacebookOutlinedIcon />, name: "Facebook" },
    { icon: <WhatsAppIcon />, name: "WhatsApp" },
    { icon: <EmailIcon />, name: "Email" },
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
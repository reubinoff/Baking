import Timeline from "@mui/lab/Timeline";
import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent, {
  timelineContentClasses,
} from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import Box from "@mui/material/Box";
import { PropTypes } from 'prop-types';

export default function RecipeTimeline(props) {
    const { items } = props;
  return (
    <Box {...props}>
      <Timeline
        position="left"
        sx={{
          [`& .${timelineContentClasses.root}`]: {
            flex: 0.2,
          },
        }}
      >
        {items.map((item) => (
          <TimelineItem key={item.val}>
            <TimelineSeparator>
              <TimelineDot variant={item.main ? "default" : "outlined"} />
              <TimelineConnector
                sx={{ display: item.connector === true ? "block" : "none" }}
              />
            </TimelineSeparator>
            <TimelineContent> {item.val} </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>
    </Box>
  );
}

RecipeTimeline.propTypes = {
    items: PropTypes.array.isRequired,
}

// items = [
//     {
//         val: "Step 1",
//         main: false,
//         connector: true,
//     }
// ]

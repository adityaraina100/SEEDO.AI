const video = document.getElementById("video");
let emailSent = {};

Promise.all([
  faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
  faceapi.nets.faceRecognitionNet.loadFromUri("/models"),
  faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
]).then(startWebcam);

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user' }, // Access the front camera of the phone
      audio: false,
    });
    video.srcObject = stream;
  } catch (error) {
    console.error(error);
  }
}

async function getLabeledFaceDescriptions() {
  const labels = [
    "Karan","Vijay"
  ]; // Add the new label here
  const labeledFaceDescriptors = [];

  for (const label of labels) {
    const descriptions = [];
    for (let i = 1; i <= 6; i++) {
      const img = await faceapi.fetchImage(`./Labels/${label}/${i}.jpg`);
      const detections = await faceapi
        .detectSingleFace(img)
        .withFaceLandmarks()
        .withFaceDescriptor();

      if (detections && detections.descriptor) {
        descriptions.push(detections.descriptor);
      } else {
        console.warn(`No face detected in image ${i} of ${label}`);
      }
    }
    if (descriptions.length > 0) {
      const labeledFaceDescriptor = new faceapi.LabeledFaceDescriptors(
        label,
        descriptions
      );
      labeledFaceDescriptors.push(labeledFaceDescriptor);
    }
  }

  return labeledFaceDescriptors;
}

async function getEmail(label) {
  const response = await fetch(`./Labels/${label}/email.txt`);
  const email = await response.text();
  return email.trim();
}

video.addEventListener("play", async () => {
  const labeledFaceDescriptors = await getLabeledFaceDescriptions();
  if (labeledFaceDescriptors.length > 0) {
    const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors);

    const canvas = faceapi.createCanvasFromMedia(video, {
      willReadFrequently: true,
    });
    document.body.append(canvas);

    const displaySize = { width: video.width, height: video.height };
    faceapi.matchDimensions(canvas, displaySize);

    const sendEmail = async (label) => {
      const labeledFaceDescriptor = labeledFaceDescriptors.find(
        (item) => item.label === label
      );
      if (
        labeledFaceDescriptor &&
        labeledFaceDescriptor.descriptors.length > 0
      ) {
        const email = await getEmail(label);
        const subject = "Attendance Update";
        const message = "Hello " + label + ", Your attendance has been marked ";

        const url = "/face-det/send_mail.php"; // Replace with the correct URL for sending the email
        const formData = new FormData();
        formData.append("email", email);
        formData.append("subject", subject);
        formData.append("message", message);

        fetch(url, {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            if (response.ok) {
              console.log("Email sent successfully to: " + email);
            } else {
              console.error("Error sending email to: " + email);
            }
          })
          .catch((error) => {
            console.error("Error sending email:", error);
          });
      }
    };

    const processResults = (results, resizedDetections) => {
      results.forEach(async (result, i) => {
        const box = resizedDetections[i].detection.box;
        const drawBox = new faceapi.draw.DrawBox(box, {
          label: result.toString(),
        });
        drawBox.draw(canvas);

        if (result.label && !emailSent[result.label]) {
          await sendEmail(result.label);
          emailSent[result.label] = true;
        }
      });
    };

    setInterval(async () => {
      const detections = await faceapi
        .detectAllFaces(video)
        .withFaceLandmarks()
        .withFaceDescriptors();

      const resizedDetections = faceapi.resizeResults(
        detections,
        displaySize
      );

      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

      const results = resizedDetections.map((d) => {
        return faceMatcher.findBestMatch(d.descriptor);
      });

      processResults(results, resizedDetections);
    }, 100);
  } else {
    console.warn(
      "No labeled face descriptors found. Face recognition may not work correctly."
    );
  }
});
